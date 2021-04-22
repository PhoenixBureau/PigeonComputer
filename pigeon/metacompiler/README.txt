Metacompiler based on META-II
===================================

As a reference the (nearly) original META-II system is in ``metaii``
subdir.

I moved the genesis of the "newlang5" language to the ``newlang5``
directory.  It follows James Neighbors' tutorial pretty closely up to the
block structure formatting, and I implement a compiler-to-Python for fun
in the ``newlang5py`` subdir, but then we stop and go in a different
direction.

We want to target the ATMega328P chip, not Python, so the block structure
isn't really necessary even.  We want the structure to remain very simple
so the runtime support on the chip can be short and sweet.  We don't need
elaborate bells and whistles (you can program the chip in C or even
MicroPython, of course!) like being able to specify token definitions in
our grammar.

I could modify the syntax to emit AVR assembly code directly, but instead
I want to target the assembler included in this project.

There's also an experimental Prolog version in ``newlang5prolog`` to
play around with code transformation.  I might replace the Python
assembler with a Prolog assembler, in any event it's easier to emit a
Prolog term describing the (abstract) ASM and then transform that into
actual assembly using simple DCGs or something.  META-II itself could be
expressed in Prolog, of course, but that seems more distant.  The whole
point of META-II is that it showcases a way to transform a
declarative(-ish) high-level language into low-level assmebly
control-flow constructs.


- - - -
Old notes:

Add new syntax from fooN.fooN to FooN+1.FooN then use it to write FooN+1.FooN+1

For the sematics output change I had to add new "asm" methods to the VM,
metaii.5.py and newlang5.newlang5 are a metacompiler with "block structure" output capability.

There's a Makefile that has the build details.
