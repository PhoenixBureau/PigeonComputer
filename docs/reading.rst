Reading a Source File
============================================

The Pigeon Assembler uses its own format for assembly source files. It's
basically a Python file that gets executed within a special context.

Miki Tebeka's Clever Idea
-------------------------

When I was researching assemblers written in Python I came across
`a fascinating blog post <http://pythonwise.blogspot.com/2012/06/python-based-assembler.html>`_
describing a very clever trick for implementing an assembler in Python.
Miki Tebeka realized that he could lean on Python itself for the usual
tasks of parsing and lexing and he managed to create a custom assembler
in just two days.

He used one class per instruction whereas I have a method and a function
for each instruction.  The assembler uses two passes and the method is
for the first while the function is for the second.
See :ref:`the internals discussion <assembler-structure>` for more
information.

The basic trick is to define callables that mimic the names of
assembler instructions and directives and then ``execfile()`` the
"assembler" source file within a context that includes them.  The
callables then create the appropriate binary output.

Source Format
-------------

The source format is pure Python and can contain pretty much any code
you want.  (As one side-effect of this, no special macro facility is
needed, instead you can simply define Python functions in your
"assembler" source and call them normally to use them.)

Here's a sample of the source format for Pigeon.  It's a simple routine
to initialize the UART perhipheral of the ATmega328P::

    label(UART_INIT)
    ldi(r16, high(520)) # 2400 baud w/ 20Mhz osc
    sts(UBRR0H, r16)
    ldi(r16, low(520))  # See Datasheet
    sts(UBRR0L, r16)
    # The chip defaults to 8N1 so we won't
    # set it here even though we should.
    ldi(r16, (1 << TXEN0) | (1 << RXEN0)) # Enable transmit/receive
    sts(UCSR0B, r16)
    ret()

As you can see, it's Python code yet it closely mimics assembly.  As each
function is executed it adds a description of the instruction to be
assembled to a datastructure maintained by the
:class:`pyavrasm.AVRAssembly` object managing the assembly process.

As an example of the pythonic nature of the assembler source code
consider the following "macro-ized" version of the above code::

    def stsi(target, immediate):
        ldi(r16, immediate)
        sts(target, r16)

    label(UART_INIT)
    stsi(UBRR0H, high(520)) # 2400 baud w/ 20Mhz osc
    stsi(UBRR0L, low(520))  # See Datasheet
    # The chip defaults to 8N1 so we won't
    # set it here even though we should.
    stsi(UCSR0B, (1 << TXEN0) | (1 << RXEN0)) # Enable transmit/receive
    ret()

You can see that the "macro" is just a Python function.  The resulting
binary code would be the same.

- - - -

Show off a comparison of Pigeon Assembler's source format,
the Amtel ASM format, and gcc ``as`` format.

