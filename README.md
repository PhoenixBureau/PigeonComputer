Pigeon Computer
===============

### From the Bare Bit to the Compiler, and Beyond...

Simple computer system built around the [ATmega328P microcontroller][1].

It is designed to be easy to use and understand at a deep level.  It was
developed to support a very hands-on course on the foundations of
commputers and programming, and as such it covers the core concepts that are
typically left out of classes on programming.

Within an elegant and powerful integrated development environment there
are:

* A simple assembler for the AVR assembly language.
* A compiler that is extremely easy to understand and extend so you can
  learn how compilers work and even develop your own custom high-level
  language(s).
* A simple and powerful Forth-like firmware that implements a
  command-line interpreter for the ATmega328P in less than a kilobyte.
* Last but not least there is a simple Tkinter GUI wrapper around simavr
  and avr-gdb that lets you step through the firmware running under gdb
  control on the simulator.  Neat..

### Links

Currently the source code is hosted on [GitHub][3] where you can download
it, report bugs, contribute to or just fork it (it's open source under
the GPL, see the `COPYING` file in the source.)

In addition to reading the source you should read the [Manual (Online
HTML version)][4] This is still in a very rough draft stage with missing
sections still to be filled in but I'm actively improving it.

### Dependencies

* MyHDL
* IntelHex
* Dulwich
* pexpect


[1]: http://www.atmel.com/devices/atmega328p.aspx

[2]: http://pythonwise.blogspot.com/2012/06/python-based-assembler.html

[3]: https://github.com/PhoenixBureau/PigeonComputer

[4]: http://phoenixbureau.github.com/PigeonComputer/
