.. _assembler-structure:

Pigeon Assembler Internals
==========================

The internal operation of the assembler is fairly straightforward.

There is a first pass where an assembly source file (which is just a
Python script containing calls to the *directives* and assembly
instructions) is executed within a special context.  This generates an
internal data structure that maps addresses to bit-pattern generators and
their associated args.

During the second pass these bit-pattern generators are called to
generate the proper binary op codes.  Addresses of labels are available
for things like adjusting the target addresses of relative instructions.


First Pass
----------

The :py:meth:`pigeon.assembler.pyavrasm.AVRAssembly.assemble` and
:py:meth:`pigeon.assembler.pyavrasm.AVRAssembly.assemble_file` methods read an
assembly-in-python source file (for example, the :ref:`Pigeon Firmware`.)

Any of the instruction methods defined in the
:py:class:`pigeon.assembler.instructions.InstructionsMixin` that are called in the source
file will create an entry in the assembler's
:py:attr:`pigeon.assembler.pyavrasm.AVRAssembly.data` dictionary.  These entries consist
of the name of the op (instruction) and the arguments that were passed to
the instruction methods.


Intermediate Representations
----------------------------


Second Pass
-----------

When you call :py:meth:`pigeon.assembler.pyavrasm.AVRAssembly.pass2` the assembler goes
through the :py:attr:`pigeon.assembler.pyavrasm.AVRAssembly.data` dictionary and calls the
bit-pattern-generating op functions with the associated arguments.  The
returned binary strings are compiled into another dictionary, keyed by
their target addresses.

This dictionary is used by the :py:meth:`pigeon.assembler.pyavrasm.AVRAssembly.to_hex`
method to generate the HEX format output.


.. automodule:: pigeon.assembler.pyavrasm


