

define(TOS=r27)
define(TOSL=r26)
define(Working=r16)
define(Base=r8)

org(SRAM_START)
buffer_length = 0x40
label(buffer, reserves=buffer_length)
label(data_stack)


# Macros.


def popup():
  ld_pre_decr(TOSL, Y)


def pushdownw():
  st_post_incr(Y, TOSL)
  st_post_incr(Y, TOS)


def popupw():
  ld_pre_decr(TOS, Y)
  ld_pre_decr(TOSL, Y)


org(0x0000)
jmp(RESET)
for _ in range(25):   # There are 25 interrupt vectors.
  jmp(BAD_INTERUPT)

label(BAD_INTERUPT)
jmp(0x0000)

label(RESET)
cli()

ldi(Working, low(RAMEND))
out(SPL, Working)
ldi(Working, high(RAMEND))
out(SPH, Working)

ldi(YL, low(data_stack))
ldi(YH, high(data_stack))

rcall(UART_INIT)

ldi(Working, 23)
sts(TWBR, Working) # set bitrate
ldi(Working, 1)
sts(TWSR, Working) # set prescaler

ldi(Working, 10)
mov(Base, Working)

sei()

label(MAIN)
rcall(INTERPRET_PFA)
rcall(DOTESS_PFA)
rjmp(MAIN)

label(UART_INIT)
ldi(r17, high(520)) # 2400 baud w/ 20Mhz osc
ldi(r16, low(520))  # See Datasheet
sts(UBRR0H, r17)
sts(UBRR0L, r16)
# The chip defaults to 8N1 so we won't set it here even though we should.
ldi(r16, (1 << TXEN0) | (1 << RXEN0)) # Enable transmit/receive
sts(UCSR0B, r16)
ret()


_last_defined_word = 0x0000
def word_header(label_, name):
  global _last_defined_word
  label(label_)
  dw(_last_defined_word >> 1)
  db(len(name), name)
  _last_defined_word = label_


word_header(KEY, "key") # = - - - - - - - - - - - -
label(KEY_PFA)
lds(Working, UCSR0A)
sbrs(Working, RXC0)
rjmp(KEY_PFA)

rcall(DUP_PFA)
lds(TOS, UDR0)

rcall(ECHO_PFA)
ret()

word_header(DUP, "dup") # = - - - - - - - - - - - -
label(DUP_PFA)
st_post_incr(Y, TOSL) # push TOSL onto data stack
mov(TOSL, TOS)
ret()

word_header(EMIT, "emit") # = - - - - - - - - - - - -
label(EMIT_PFA)
rcall(ECHO_PFA)
rcall(DROP_PFA)
ret()

word_header(ECHO, "echo") # = - - - - - - - - - - - -
label(ECHO_PFA)
lds(Working, UCSR0A)
sbrs(Working, UDRE0)
rjmp(ECHO_PFA)

sts(UDR0, TOS)
ret()

word_header(DROP, "drop") # = - - - - - - - - - - - -
label(DROP_PFA)
mov(TOS, TOSL)
popup()
ret()

word_header(WORD, "word") # = - - - - - - - - - - - -
label(WORD_PFA)
rcall(KEY_PFA)

cpi(TOS, ' ')
brne(_a_key)

rcall(DROP_PFA)
rjmp(WORD_PFA)

label(_a_key)
ldi(ZL, low(buffer))
ldi(ZH, high(buffer))
ldi(word_counter, 0x00)

label(_find_length)
cpi(word_counter, 0x40)
breq(_a_key)

st_post_incr(Z, TOS)
rcall(DROP_PFA)
inc(word_counter)

rcall(KEY_PFA)
cpi(TOS, ' ')
brne(_find_length)

mov(TOS, word_counter)
ret()

word_header(NUMBER, "number") # = - - - - - - - - - - - -
label(NUMBER_PFA)

ldi(ZL, low(buffer))
ldi(ZH, high(buffer))

mov(number_pointer, TOS)
ldi(Working, 0x00)
ld_post_incr(TOS, Z)
rjmp(_convert)

label(_convert_again)
mul(Working, Base)
mov(Working, r0)
ld_post_incr(TOS, Z)

label(_convert)

cpi(TOS, '0')
brlo(_num_err)
cpi(TOS, ':') # the char after '9'
brlo(_decimal)

rjmp(_num_err)

label(_decimal)
subi(TOS, '0')
rjmp(_converted)

label(_num_err)
st_post_incr(Y, TOSL)
mov(TOSL, TOS)
mov(TOS, number_pointer)
ret()

label(_converted)
add(Working, TOS)
dec(number_pointer)
brne(_convert_again)

st_post_incr(Y, TOSL)
mov(TOSL, Working)
mov(TOS, number_pointer)
ret()

word_header(LEFT_SHIFT_WORD, "<<w") # = - - - - - - - - - - - -
label(LEFT_SHIFT_WORD_PFA)
mov(Working, TOS)
clr(TOS)
lsl(TOSL)

brcc(_lslw0)
inc(TOS) # copy carry flag to TOS[0]
label(_lslw0)
lsl(Working)
or_(TOS, Working)

ret()

label(HEXDIGITS) ; db("0123456789abcdef")

word_header(EMIT_HEX, "emithex") # = - - - - - - - - - - - -
label(EMIT_HEX_PFA)

push(ZH)
push(ZL)

rcall(DUP_PFA)
swap(TOS)
rcall(emit_nibble) # high
rcall(emit_nibble) # low

pop(ZL)
pop(ZH)
ret()

label(emit_nibble)

pushdownw()
ldi(TOS, high(HEXDIGITS))
ldi(TOSL, low(HEXDIGITS))
rcall(LEFT_SHIFT_WORD_PFA)
movw(Z, X)
popupw()

andi(TOS, 0x0f)

label(_eloop)
cpi(TOS, 0x00)

breq(_edone)
dec(TOS)

adiw(Z, 1)
rjmp(_eloop)

label(_edone)

lpm(TOS, Z)
rcall(EMIT_PFA)
ret()

word_header(DOTESS, ".s") # = - - - - - - - - - - - -
label(DOTESS_PFA)

rcall(DUP_PFA)

ldi(TOS, 0x0d) # CR
rcall(ECHO_PFA)
ldi(TOS, 0x0a) # LF
rcall(ECHO_PFA)
ldi(TOS, '[')
rcall(ECHO_PFA)

mov(TOS, TOSL)
rcall(EMIT_HEX_PFA)

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

movw(Z, Y)
rcall(DUP_PFA)

label(_inny)

ldi(Working, low(data_stack))
cp(ZL, Working)
ldi(Working, high(data_stack))
cpc(ZH, Working)
brsh(_itsok)

ldi(TOS, ']')
rcall(ECHO_PFA)
ldi(TOS, 0x0d) # CR
rcall(ECHO_PFA)
ldi(TOS, 0x0a) # LF
rcall(EMIT_PFA)
ret()

label(_itsok)
ld_pre_decr(TOS, Z)
rcall(EMIT_HEX_PFA)
rcall(DUP_PFA)
ldi(TOS, ' ')
rcall(ECHO_PFA)

rjmp(_inny)

word_header(FIND, "find") # = - - - - - - - - - - - -
label(FIND_PFA)

mov(word_counter, TOS)
st_post_incr(Y, TOSL)
ldi(TOSL, low(READ_IMU))
ldi(TOS, high(READ_IMU))

label(_look_up_word)
cpi(TOSL, 0x00)
brne(_non_zero)
cpse(TOSL, TOS)
rjmp(_non_zero)

ldi(TOS, 0xff)
ldi(TOSL, 0xff)
ret()

label(_non_zero)

pushdownw()

rcall(LEFT_SHIFT_WORD_PFA)
movw(Z, X)
lpm_post_incr(TOSL, Z)
lpm_post_incr(TOS, Z)

lpm_post_incr(Working, Z)
cp(Working, word_counter)
breq(_same_length)

sbiw(Y, 2)
rjmp(_look_up_word)

label(_same_length)
pushdownw()
ldi(TOS, high(buffer))
ldi(TOSL, low(buffer))

label(_compare_name_and_target_byte)
ld_post_incr(find_buffer_char, X) # from buffer
lpm_post_incr(find_name_char, Z) # from program RAM
cp(find_buffer_char, find_name_char)
breq(_okay_dokay)

popupw() # ditch search term address
sbiw(Y, 2) # ditch LFA_current
rjmp(_look_up_word)

label(_okay_dokay)
dec(Working)
brne(_compare_name_and_target_byte)

popupw() # ditch search term address
popupw() # ditch LFA_next
ret() # LFA_current

word_header(TPFA, ">pfa") # = - - - - - - - - - - - -
label(TPFA_PFA)

adiw(X, 1)
pushdownw() # save address
rcall(LEFT_SHIFT_WORD_PFA)

movw(Z, X)
lpm(Working, Z)
popupw() # restore address

lsr(Working)
inc(Working)       # n <- (n >> 1) + 1
add(TOSL, Working) # Add the adjusted name length to our prog mem pointer.
brcc(_done_adding)
inc(TOS)           # Account for the carry bit if set.
label(_done_adding)
ret()

word_header(INTERPRET, "interpret") # = - - - - - - - - - - - -
label(INTERPRET_PFA)

rcall(WORD_PFA)

mov(temp_length, TOS)

rcall(NUMBER_PFA)
cpi(TOS, 0x00) # all chars converted?
brne(_maybe_word)

mov(TOS, TOSL)
popup()
ret()

label(_maybe_word)
mov(TOS, temp_length)
popup()
rcall(FIND_PFA)

cpi(TOS, 0xff)
brne(_is_word)

popup()
ldi(TOS, '?')
rcall(EMIT_PFA)
ret()

label(_is_word)
rcall(TPFA_PFA)
movw(Z, X)
popupw()
ijmp()

