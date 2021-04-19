Metacompiler based on META-II
===================================

I moved the genesis of the "newlang5" language to the ``/prelude``
directory.  It follows James Neighbors' tutorial pretty closely up to the
block structure formatting, and I implement a compiler-to-Python for fun,
but then we stop and go in a different direction.

We want to target the ATMega328P chip, not Python, so the block structure
isn't really necessary even.  We want the structure to remain very simple
so the runtime support on the chip can be short and sweet.  We don't need
elaborate bells and whistles (you can program the chip in C or even
MicroPython, of course!) like being able to specify token definitions in
our grammar.



- - - -
Old notes:

Add new syntax from fooN.fooN to FooN+1.FooN then use it to write FooN+1.FooN+1

For the sematics output change I had to add new "asm" methods to the VM,
metaii.5.py and newlang5.newlang5 are a metacompiler with "block structure" output capability.

There's a Makefile that has the build details.
