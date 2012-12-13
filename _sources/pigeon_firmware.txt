.. _Pigeon Firmware:

===============
Pigeon Firmware
===============

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


.. contents::


Introduction
------------

This is a simple Forth-like firmware for `ATmega328P`_ micro-controllers.

The system in general probably won't make much sense unless you're
already at least a little familiar with Forth. Two helpful sources are
`Brad Rodriguez' "Moving Forth" series`_ and `Richard
Jones'`_ wonderful `jonesforth "literate Forth"`_.

There's no attempt to implement or adhere to any standard Forth. I'm just
noodling around and creating the easiest version of whatever seems like it
will work.  It's also my first attempt at writing assembly code in over
a decade, and the first time using AVR assembly, so there are certainly
going to be some, uh, less-than-perfect code. Please bear with me.

.. _ATmega328P: http://www.atmel.com/devices/atmega328p.aspx

.. _Pololu Baby Orangutan robot controller: http://www.pololu.com/catalog/product/1220

.. _Brad Rodriguez' "Moving Forth" series: http://www.bradrodriguez.com/papers/moving1.htm

.. _jonesforth "literate Forth": http://git.annexia.org/?p=jonesforth.git;a=summary

.. _Richard Jones': http://rwmj.wordpress.com/2010/08/07/jonesforth-git-repository/


Definitions
-----------

Let's start by creating some definitions for various registers the system
will use.


The Data Stack
^^^^^^^^^^^^^^

The AVR chip has a Harvard architecture with separate memories and buses for
program and data RAM. The data bus, SRAM, and registers are eight bits wide,
while the address bus and Flash memory (for persistent program storage)
are sixteen bits wide.

I've decided to try having the Top-Of-Stack (TOS) and the next 8-bit
"cell" underneath it (which I call TOSL below) in two registers with the
rest of the stack pointed to by another pair of registers.

Certain pairs of 8-bit registers (namely the "top" six registers r26 -
r31) can be used as 16-bit registers (namely X, Y, and Z) for addressing
and some math functions

If we use a pair of such registers as our TOS and TOSL it gives us the
ability to, say, put the low and high bytes of an address in program or
data RAM onto the stack and then efficiently use the 16-bit value to
fetch or store from that location.

Keep the top two items (bytes) on the stack in the X register::

  define(TOS=r27)
  define(TOSL=r26)

Y register is our Data Stack Pointer.


Other Register Assignments
^^^^^^^^^^^^^^^^^^^^^^^^^^

Z register will be used for diggin around in the dictionary.

We also use a working register::

  define(Working=r16)

The "word" word needs to track how many bytes it has read. This is also
reused by find::

  define(word_counter=r17)

Base (numeric base for converting digits to numbers)::

  define(Base=r8)

Number keeps track of the digits it is converting using this register::

  define(number_pointer=r9)

Registers used by FIND word::

  define(find_buffer_char=r10)
  define(find_name_char=r11)

Register used by Interpret::

  define(temp_length=r12)



Data (SRAM) Organization
------------------------

On the 328P the first 256 bytes of data space are actually the registers
and I/O ports (see the Datasheet for details)::

  org(SRAM_START)

Word Buffer
^^^^^^^^^^^

The "word" word reads the stream of characters returned by the "key" word
and fills this buffer until it reaches a space character. It's only 64
bytes because we're going to be using a single-byte length field and
packing two bits of meta-data into it, leaving six bits to specify the
word length, giving us a maximum possible name length of sixty-four::


  buffer_length = 0x40
  label(buffer, reserves=buffer_length)


Data Stack
^^^^^^^^^^

The Parameter (Data) Stack grows upward
towards the Return Stack at the top of RAM. Note that the first two bytes
of stack are kept in the X register. Due to this the initial two bytes of
the data stack will be filled with whatever was in X before the first
push, unless you load X (i.e. TOS and Just-Under-TOS) "manually" before
dropping into the interpreter loop::

  label(data_stack)



Code (Flash RAM)
----------------

Macros
^^^^^^

Some data stack manipulation macros to ease readability.

Pop from data stack to TOSL. Note that you are responsible for preserving
the previous value of TOSL if you still want it after using the macro.
(I.e. mov TOS, TOSL)::

  # Macros.

  def popup():
    ld_pre_decr(TOSL, Y)

Make room on TOS and TOSL by pushing them onto the data stack::

  def pushdownw():
    st_post_incr(Y, TOSL)
    st_post_incr(Y, TOS)

Essentially "drop drop"::

  def popupw():
    ld_pre_decr(TOS, Y)
    ld_pre_decr(TOSL, Y)



Begining of code proper
^^^^^^^^^^^^^^^^^^^^^^^

::

  org(0x0000)
  jmp(RESET)

Interupt Vectors
^^^^^^^^^^^^^^^^

::

  for _ in range(25):   # There are 25 interrupt vectors.
    jmp(BAD_INTERUPT)

  label(BAD_INTERUPT)
  jmp(0x0000)


Initial reset vector
^^^^^^^^^^^^^^^^^^^^

Disable interrupts and reset everything::

  label(RESET)
  cli()

Set up the Return Stack::

  ldi(Working, low(RAMEND))
  out(SPL, Working)
  ldi(Working, high(RAMEND))
  out(SPH, Working)

Initialize Data Stack::

  ldi(YL, low(data_stack))
  ldi(YH, high(data_stack))

Set the UART to talk to a serial port::

  rcall(UART_INIT)

Set up 100kHz freq for TWI/I2C peripheral::

  ldi(Working, 23)
  sts(TWBR, Working) # set bitrate
  ldi(Working, 1)
  sts(TWSR, Working) # set prescaler

Initialize Base::

  ldi(Working, 10)
  mov(Base, Working)

Re-enable interrupts::

  sei()

TODO: Set up a Stack Overflow Handler and put its address at RAMEND
and set initial stack pointer to RAMEND - 2 (or would it be 1?)
That way if we RET from somewhere and the stack is underflowed we'll
trigger the handler instead of just freaking out.

Main Loop
^^^^^^^^^

Our (very simple) main loop just calls "quit" over and over again::

  label(MAIN)
  rcall(INTERPRET_PFA)
  rcall(DOTESS_PFA)
  rjmp(MAIN)

Initialize the USART
^^^^^^^^^^^^^^^^^^^^

::

  label(UART_INIT)
  ldi(r17, high(520)) # 2400 baud w/ 20Mhz osc
  ldi(r16, low(520))  # See Datasheet
  sts(UBRR0H, r17)
  sts(UBRR0L, r16)
  # The chip defaults to 8N1 so we won't set it here even though we should.
  ldi(r16, (1 << TXEN0) | (1 << RXEN0)) # Enable transmit/receive
  sts(UCSR0B, r16)
  ret()


Words
-----

These are the basic commands of the system that work together to
implement the interpreter. We define a macro to automatically
generate word headers::

  _last_defined_word = 0x0000
  def word_header(label_, name):
    global _last_defined_word
    label(label_)
    dw(_last_defined_word >> 1)
    db(len(name), name)
    _last_defined_word = label_

Key
^^^^^

Read a character from the serial port and push it onto the stack::

  word_header(KEY, "key") # = - - - - - - - - - - - -

First, loop on the RXC0 bit of the UCSR0A register, which indicates that
a byte is available in the receive register::

  label(KEY_PFA)
  lds(Working, UCSR0A)
  sbrs(Working, RXC0)
  rjmp(KEY_PFA)

Make room on the stack and load the character onto it from the UART's data register::

  rcall(DUP_PFA)
  lds(TOS, UDR0)

Echo the char to the serial port::

  rcall(ECHO_PFA)
  ret()

Dup
^^^^^

Duplicate the top value on the stack::

  word_header(DUP, "dup") # = - - - - - - - - - - - -
  label(DUP_PFA)
  st_post_incr(Y, TOSL) # push TOSL onto data stack
  mov(TOSL, TOS)
  ret()

Emit
^^^^^

Pop the top item from the stack and send it to the serial port::

  word_header(EMIT, "emit") # = - - - - - - - - - - - -
  label(EMIT_PFA)
  rcall(ECHO_PFA)
  rcall(DROP_PFA)
  ret()

Echo
^^^^^

Write the top item on the stack to the serial port::

  word_header(ECHO, "echo") # = - - - - - - - - - - - -

First, loop on the UDRE0 bit of the UCSR0A register, which indicates that
the data register is ready for a byte::

  label(ECHO_PFA)
  lds(Working, UCSR0A)
  sbrs(Working, UDRE0)
  rjmp(ECHO_PFA)

When it's ready, write the byte to the UART data register::

  sts(UDR0, TOS)
  ret()

Drop
^^^^^

Drop the top item from the stack::

  word_header(DROP, "drop") # = - - - - - - - - - - - -
  label(DROP_PFA)
  mov(TOS, TOSL)
  popup()
  ret()

Word
^^^^^

Now that we can receive bytes from the serial port, the next step is a
"word" word that can parse space (hex 0x20) character-delimited words
from the stream of incoming chars.::

  word_header(WORD, "word") # = - - - - - - - - - - - -
  label(WORD_PFA)

Get next char onto stack::

  rcall(KEY_PFA)

Is it a space character?::

  cpi(TOS, ' ')
  brne(_a_key)

Then drop it from the stack and loop to get the next character::

  rcall(DROP_PFA)
  rjmp(WORD_PFA)

If it's not a space character then begin saving chars to the word buffer.
Set up the Z register to point to the buffer and reset the word_counter::

  label(_a_key)
  ldi(ZL, low(buffer))
  ldi(ZH, high(buffer))
  ldi(word_counter, 0x00)

First, check that we haven't overflowed the buffer. If we have, silently
"restart" the word, and just ditch whatever went before.::

  label(_find_length)
  cpi(word_counter, 0x40)
  breq(_a_key)

Save the char to the buffer and clear it from the stack::

  st_post_incr(Z, TOS)
  rcall(DROP_PFA)
  inc(word_counter)

Get the next character, breaking if it's a space character (hex 0x20)::

  rcall(KEY_PFA)
  cpi(TOS, ' ')
  brne(_find_length)

A space was found, copy length to TOS::

  mov(TOS, word_counter)
  ret()
      
Number
^^^^^^

Parse a number from the word_buffer. The length of the word is in TOS.
Return the number of characters unconverted in TOS and the value, or
first unconverted character, in TOSL::

  word_header(NUMBER, "number") # = - - - - - - - - - - - -
  label(NUMBER_PFA)

Point Z at the buffer::

  ldi(ZL, low(buffer))
  ldi(ZH, high(buffer))

We'll accumulate the number in Working. Set it to zero.
Then save the length to number_pointer and load the first character into
TOS::

  mov(number_pointer, TOS)
  ldi(Working, 0x00)
  ld_post_incr(TOS, Z)
  rjmp(_convert)

This is where we loop back in if there is more than one digit to convert.
We multiply the current accumulated value by the Base (the 16-bit result
is placed in r1:r0) and load the next digit into TOS::

  label(_convert_again)
  mul(Working, Base)
  mov(Working, r0)
  ld_post_incr(TOS, Z)

  label(_convert)

If the character is between '0' and '9' go to _decimal::

  cpi(TOS, '0')
  brlo(_num_err)
  cpi(TOS, ':') # the char after '9'
  brlo(_decimal)

  rjmp(_num_err)

For a decimal digit, just subtract '0' from the char to get the value::

  label(_decimal)
  subi(TOS, '0')
  rjmp(_converted)

If we encounter an unknown digit put the number of remaining unconverted
digits into TOS and the unrecognized character in TOSL::

  label(_num_err)
  st_post_incr(Y, TOSL)
  mov(TOSL, TOS)
  mov(TOS, number_pointer)
  ret()

Once we have a digit in TOS we can add it to our accumulator and, if
there are more digits to convert, we loop back to keep converting them::

  label(_converted)
  add(Working, TOS)
  dec(number_pointer)
  brne(_convert_again)

We're done, move the result to TOSL and zero, signaling successful
conversion, in TOS::

  st_post_incr(Y, TOSL)
  mov(TOSL, Working)
  mov(TOS, number_pointer)
  ret()

Left Shift Word (16-Bit) Value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The AVR chip has a slight wrinkle when accessing program (flash) RAM.
Because it is organized in 16-bit words there are 16K addresses to
address the 32K of RAM. The architecture allows for reaching each byte
by means of left-shifting the address and using the least significant
bit to indicate low (0) or high (1) byte.

This means that if we get an address from e.g. the return stack and
we want to access data in program RAM with it we have to shift it one
bit left. This word "<<w" shifts a 16-bit value in TOS:TOSL one bit to
the left::

  word_header(LEFT_SHIFT_WORD, "<<w") # = - - - - - - - - - - - -
  label(LEFT_SHIFT_WORD_PFA)
  mov(Working, TOS)
  clr(TOS)
  lsl(TOSL)

If the carry bit is clear skip incrementing TOS::

  brcc(_lslw0)
  inc(TOS) # copy carry flag to TOS[0]
  label(_lslw0)
  lsl(Working)
  or_(TOS, Working)

X now contains left-shifted word, and carry bit reflects TOS carry::

  ret()

Emithex
^^^^^^^

I want to be able to emit values (from the stack or wherever) as hex
digits. This word pops the value on the stack and writes it to the serial
port as two hex digits (high byte first)::

  label(HEXDIGITS) ; db("0123456789abcdef")

  word_header(EMIT_HEX, "emithex") # = - - - - - - - - - - - -
  label(EMIT_HEX_PFA)

Save Z register onto the return stack::

  push(ZH)
  push(ZL)

Dup TOS, emit the low byte, then the high byte::

  rcall(DUP_PFA)
  swap(TOS)
  rcall(emit_nibble) # high
  rcall(emit_nibble) # low

Restore Z from the return stack::

  pop(ZL)
  pop(ZH)
  ret()

So now to emit nybbles. This routine consumes TOS and clobbers Z::

  label(emit_nibble)

Get the address of HEXDIGITS into Z::

  pushdownw()
  ldi(TOS, high(HEXDIGITS >> 1))
  ldi(TOSL, low(HEXDIGITS >> 1))
  rcall(LEFT_SHIFT_WORD_PFA)
  movw(Z, X)
  popupw()

mask high nibble::

  andi(TOS, 0x0f)

Since there's no direct way to add the nibble to Z (I could define a
16-bit-plus-8-bit add word, and I probably will later) we'll use a loop
and the adiw instruction::

  label(_eloop)
  cpi(TOS, 0x00)

If nibble is not zero...::

  breq(_edone)
  dec(TOS)

Increment the HEXDIGITS pointer::

  adiw(Z, 1)
  rjmp(_eloop)

  label(_edone)

Z points at correct char::

  lpm(TOS, Z)
  rcall(EMIT_PFA)
  ret()


.S
^^^^^

Print out the stack::

  word_header(DOTESS, ".s") # = - - - - - - - - - - - -
  label(DOTESS_PFA)

Make room on the stack::

  rcall(DUP_PFA)

Print out 'cr' 'lf' '['::

  ldi(TOS, 0x0d) # CR
  rcall(ECHO_PFA)
  ldi(TOS, 0x0a) # LF
  rcall(ECHO_PFA)
  ldi(TOS, '[')
  rcall(ECHO_PFA)

Print (as hex) TOS and TOSL. First copy TOSL to TOS to get the value back
but leave the stack at the same depth, then call emithex which will pop
a value::

  mov(TOS, TOSL)
  rcall(EMIT_HEX_PFA)

Now we're back to where we started.::

  mov(Working, TOSL)
  rcall(DUP_PFA )     # tos, tos, tosl
  mov(TOS, Working)   # tosl, tos, tosl
  rcall(DUP_PFA)      # tosl, tosl, tos, tosl
  ldi(TOS, '-')       # '-', tosl, tos, tosl
  rcall(EMIT_PFA)     # tosl, tos, tosl
  rcall(EMIT_HEX_PFA) # tos, tosl

  rcall(DUP_PFA)  # tos, tos, tosl
  ldi(TOS, ' ')   # ' ', tos, tosl
  rcall(EMIT_PFA) # tos, tosl

Point Z at the top of the stack (the part of the stack "under" TOS and
TOSL)::

  movw(Z, Y)
  rcall(DUP_PFA)

  label(_inny)

If the Z register is the same as or higher than data_stack print the
item at Z::

  ldi(Working, low(data_stack))
  cp(ZL, Working)
  ldi(Working, high(data_stack))
  cpc(ZH, Working)
  brsh(_itsok)

Otherwise, we're done::

  ldi(TOS, ']')
  rcall(ECHO_PFA)
  ldi(TOS, 0x0d) # CR
  rcall(ECHO_PFA)
  ldi(TOS, 0x0a) # LF
  rcall(EMIT_PFA)
  ret()

Load the value at (pre-decremented) Z and emit it as hex::

  label(_itsok)
  ld_pre_decr(TOS, Z)
  rcall(EMIT_HEX_PFA)
  rcall(DUP_PFA)
  ldi(TOS, ' ')
  rcall(ECHO_PFA)

And go to the next one::

  rjmp(_inny)


Find
^^^^^

Given the length of a word in the word_buffer, find attempts to find that
word in the dictionary and return its LFA on the stack (in TOS:TOSL).
If the word can't be found, put 0xffff into TOS:TOSL::

  word_header(FIND, "find") # = - - - - - - - - - - - -

Make room on the stack for address::

  label(FIND_PFA)

  mov(word_counter, TOS)
  st_post_incr(Y, TOSL)

  # Define this "manually" here to compensate for the fact that high() and
  # low() below will compute and return their results immediately rather
  # than during pass 2  Should FIXME in the future.
  DICTIONARY_START = 0x2a0

  ldi(TOSL, low(DICTIONARY_START))
  ldi(TOS, high(DICTIONARY_START))

Check if TOS:TOSL == 0x0000::

  label(_look_up_word)
  cpi(TOSL, 0x00)
  brne(_non_zero)
  cpse(TOSL, TOS)
  rjmp(_non_zero)

if TOS:TOSL == 0x0000 we're done::

  ldi(TOS, 0xff)
  ldi(TOSL, 0xff)
  ret()

While TOS:TOSL != 0x0000 check if this it the right word::

  label(_non_zero)

Save current Link Field Address::

  pushdownw()

Load Link Field Address of next word in the dictionary into the X
register pair::

  rcall(LEFT_SHIFT_WORD_PFA)
  movw(Z, X)
  lpm_post_incr(TOSL, Z)
  lpm_post_incr(TOS, Z)

Now stack has ( - LFA_next, LFA_current) Load length-of-name byte into a register::

  lpm_post_incr(Working, Z)
  cp(Working, word_counter)
  breq(_same_length)

Not the same length, ditch LFA_current and loop::

  sbiw(Y, 2)
  rjmp(_look_up_word)

If they're the same length walk through both and compare them character
by character.

Length is in Working and word_counter. Z holds current word's name's
first byte's address in program RAM. TOS:TOSL have the address of the
next word's LFA. So stack has ( - LFA_next, LFA_current)

Put address of search term in buffer into X (TOS:TOSL)::

  label(_same_length)
  pushdownw()
  ldi(TOS, high(buffer))
  ldi(TOSL, low(buffer))

stack ( - buffer, LFA_next, LFA_current)::

  label(_compare_name_and_target_byte)
  ld_post_incr(find_buffer_char, X) # from buffer
  lpm_post_incr(find_name_char, Z) # from program RAM
  cp(find_buffer_char, find_name_char)
  breq(_okay_dokay)

Not equal, clean up and go to next word::

  popupw() # ditch search term address
  sbiw(Y, 2) # ditch LFA_current
  rjmp(_look_up_word)

The chars are the same::

  label(_okay_dokay)
  dec(Working)
  brne(_compare_name_and_target_byte)

If we get here we've checked that every character in the name and the
target term match::

  popupw() # ditch search term address
  popupw() # ditch LFA_next
  ret() # LFA_current


To PFA
^^^^^^

">pfa" Given a word's LFA (Link Field Address) in TOS:TOSL, find its PFA::

  word_header(TPFA, ">pfa") # = - - - - - - - - - - - -
  label(TPFA_PFA)

Point to name length and adjust the address::

  adiw(X, 1)
  pushdownw() # save address
  rcall(LEFT_SHIFT_WORD_PFA)

get the length::

  movw(Z, X)
  lpm(Working, Z)
  popupw() # restore address

We need to map from length in bytes to length in words while allowing
for the padding bytes in even-length names::

  lsr(Working)
  inc(Working)       # n <- (n >> 1) + 1
  add(TOSL, Working) # Add the adjusted name length to our prog mem pointer.
  brcc(_done_adding)
  inc(TOS)           # Account for the carry bit if set.
  label(_done_adding)
  ret()


interpret
^^^^^^^^^

::

  word_header(INTERPRET, "interpret") # = - - - - - - - - - - - -
  label(INTERPRET_PFA)

get length of word in buffer::

  rcall(WORD_PFA)

save length::

  mov(temp_length, TOS)

Is it a number?::

  rcall(NUMBER_PFA)
  cpi(TOS, 0x00) # all chars converted?
  brne(_maybe_word)

Then leave it on the stack::

  mov(TOS, TOSL)
  popup()
  ret()

Otherwise, put length back on TOS and call find::

  label(_maybe_word)
  mov(TOS, temp_length)
  popup()
  rcall(FIND_PFA)

Did we find the word?::

  cpi(TOS, 0xff)
  brne(_is_word)

No? Emit a '?' and be done with it::

  popup()
  ldi(TOS, '?')
  rcall(EMIT_PFA)
  ret()

We found the word, execute it::

  label(_is_word)
  rcall(TPFA_PFA)
  movw(Z, X)
  popupw()
  ijmp()


Conclusion
----------

So that is a useful not-quite-Forth interpreter. I've burned this
program to my Pololu Baby Orangutan and it runs. I can connect to it
over a serial connection to pins PD0 and PD1 (I'm using the Pololu USB
AVR programmer and its built in USB-to-TTL-compatible serial port.)

The following thirteen words are defined above:

- Key
- Emit
- Echo
- Drop
- Word
- Number
- <<w (Left Shift 16-bit Word)
- Emithex
- .s
- Find
- >pfa (To PFA)
- Interpret

Not bad for 716 bytes of machine code.

To me it is exciting and even a bit incredible to be communicating to a
chip smaller than (for instance) the pupil of my eye using a simple but
effective command line interface that fits within one kilobyte of code.


Program-ability
^^^^^^^^^^^^^^^

The main difference between this engine and a real Forth is that AVRVM
can't compile new words.

In a more typical (or really, more original) Forth target architecture,
the data and program RAM are not separate, and you could easily lay down
new words in memory and immediately use them.

With the split Harvard architecture of the AVR the program RAM is flash
and can only be written to about a thousand times before risking
degradation. (There is a 1K block of EEPROM memory which can be
erased/written up to about 100,000 times. I'm ignoring it for now but
hope to use it somehow in the future.)

Since the data SRAM has only 2K, and since you can't directly execute
code bytes from it, there's not really a lot of room for compiling words
there.

We can compile words there and use the SPM instruction to copy them to
flash RAM, and I plan to write some words to enable that at some point,
but it makes a lot more sense to use the rest of the 32K program memory
to include "libraries" of additional routines (Forth words) written in
assembler (or C with proper interfacing) that can then be "driven" by
small "scripts" stored in SRAM.

The main drawback of this method could be the inability to debug commands
(words) as you write them. But with careful coding and use of the
simulator we should be able to develop stable commands without "burning
out" too many processors (with Flash rewrites.)


