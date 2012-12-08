Pigeon Computer
===============

Simple computer system built around the [ATmega328P microcontroller][1].

It is designed to be easy to use and understand at a deep level.

There is a simple assembler, written in Python, for the AVR
assembly language.  It is built along the ideas of Miki Tebeka  and his
fascinating [Python based assembler][2] although with a slightly
different architecture.  The basic trick of interpreting a python file
in a special context to get parsing &c. for free is the same.

There is a compiler that is extremely easy to understand and extend so
you can learn how compilers work and even develop your own custom high-level
language(s).

There is also a simple and powerful Forth-like firmware that implements
a command-line interpreter for the ATmega328P in less than a kilobyte.

Last but not least there is a simple Tkinter GUI wrapper around simavr
and avr-gdb that lets you step through the firmware running under gdb
control on the simulator.  Neat..

### Dependencies

* MyHDL
* IntelHex
* pexpect


[1]: http://www.atmel.com/devices/atmega328p.aspx

[2]: http://pythonwise.blogspot.com/2012/06/python-based-assembler.html

