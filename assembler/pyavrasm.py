#!/usr/bin/env python
'''
====================
Python AVR Assembler
====================

This is the Pigeon Assembler.
'''
import pprint, logging
log = logging.getLogger('ASM')
logging.basicConfig()
from collections import defaultdict
from struct import pack
from myhdl import intbv
from instructions import InstructionsMixin
from util import (
  update,
  int2addr,
  ibv,
  low,
  high,
  compute_dw,
  compute_db,
  )


class DirectivesMixin(object):
  '''
  These are *directives*, assembler functions that don't correspond to op
  codes but instead do some sort of other function.
  '''

  def define(self, **defs):
    '''
    Update one or more names in the execution namespace.  The main
    difference between using this function and simply setting a variable
    in your asm code is that this function automatically converts
    integer value(s) into ``intbv`` object(s).

    :param defs: ``<name>=<value>`` pairs
    :rtype: ``None``
    '''
    for k, v in defs.iteritems():
      if isinstance(v, int):
        defs[k] = v = ibv(v)
      log.debug('defining %s = %#x', k, v)
    self.context.update(defs)

  def org(self, address):
    '''
    Set the current output address of the assembly process to
    ``address``.  If ``address`` isn't an ``intbv`` it is converted to
    one.

    :param address: Location in program.
    :type address: ``intbv``, ``int``, or symbolic label.
    :rtype: ``None``
    '''
    address = ibv(address)
    log.debug('setting org to %#06x', address)
    update(self.here, address)

  def label(self, label_thunk, reserves=0):
    '''
    Create a symbolic label at the current output address of the assembly
    process. If ``reserves`` is given (and greater than zero) that many
    bytes are reserved by adding the value to the current output address.

    :param label_thunk: An ``intbv`` object serving as a container for a
       pointer value to an address in your assembly program.

       When you mention a previously unused name in your asm code the
       execution context will automatically provide that name with a new
       ``intbv`` object initialized to zero.

       Because this ``intbv`` object will be (re-)used in other parts of
       your program wherever the name is used it becomes a container for
       the eventual value (a thunk) of the address.

       When you use this *directive* with a given named address thunk
       (label) it fills in the value of the current output address of the
       assembly process.
    :type label_thunk: ``intbv``
    :param reserves: Reserve this many bytes by increasing the current
       output address of the assembly process.
    :type reserves: ``int``
    :rtype: ``None``
    '''
    assert isinstance(label_thunk, intbv), repr(label_thunk)
    assert label_thunk == 0, repr(label_thunk)
    name = self._name_of_address_thunk(label_thunk)
    log.debug('label %s => %#06x', name, self.here)
    update(label_thunk, self.here)
    if reserves:
      assert reserves > 0, repr(reserves)
      self.here += reserves

  def dw(self, *values):
    '''
    Lay down unsigned 16-bit integer values in the program image.

    :param values: Integer values to assemble.
    :type values: iterable of ``int``
    :rtype: ``None``
    '''
    addr = self._get_here()
    data = compute_dw(values)
    nbytes = len(data)
    log.debug('assembling %i data words at %s for %s => %r',
              nbytes/2, addr, values, data)
    self.data[addr] = ('dw', values, data)
    self.here += nbytes

  def db(self, *values):
    '''
    Lay down bytes in the program image. Integers 0 <= n <= 255 and
    strings are accepted.

    :param values: Values to assemble.
    :type values: iterable of ``int`` and/or ``string`` values
    :rtype: ``None``
    '''
    addr = self._get_here()
    data = compute_db(values)
    nbytes = len(data)
    log.debug('assembling %i data bytes at %s for %s => %r',
              nbytes, addr, values, data)
    self.data[addr] = ('db', values, data)
    self.here += nbytes

  def _directives(self):
    for n in dir(DirectivesMixin):
      if n.startswith('_'):
        continue
      yield n, getattr(self, n)


class AVRAssembly(InstructionsMixin, DirectivesMixin, object):
  '''
  This is the primary assembler object.  It is created out of the
  InstructionsMixin and DirectivesMixin, which together define the
  functions that you use in your assembly code, and the methods in this
  class which run the assembly proper.

  Assembling a file is a two-pass process.

  First, the text of the asm
  code is passed to the ``assemble()`` method (or you can pass a file name
  to ``assemble_file()``) which builds up an internal model of the op
  codes to be assembled.

  Second, you call ``pass2()`` which converts the internal model of the
  op codes to be assembled into a dictionary that maps addresses in the
  output machine code to the byte strings of the data that should reside
  at those addresses.

  Then you're probably going to want to call the ``to_hex()`` method to
  get that binary data out as (the contents of) a hex file, suitable for
  writing to your ATmega328P.

  When you create an :py:class:`AVRAssembly` object you can pass an
  initial_context object, a ``dict`` or anything that can be passed to
  ``dict.update()``, and it will be added to the execution context for
  your asm code.  Typically you would pass :py:obj:`m328P_def.defs` to
  include those definition for your code to use.

  :param initial_context: Context to include to make things available
     to your assembler code.  (:py:obj:`m328P_def.defs` or some other
     useful functions for example.)
  :type initial_context: ``dict`` or anything that can be passed to
     ``dict.update()``

  '''

  def __init__(self, initial_context=None):

    #: This is the execution context for your assembly file.  It is used
    #: as the namespace for ``exec`` or ``execfile`` for parsing and
    #: running your code.
    #:
    #: Because it's a ``defaultdict`` and the default factory function
    #: returns ``intbv`` objects **any** name (identifier) that you use
    #: in your code that is not previously defined will automatically
    #: generate a new variable binding.
    #:
    #: That is how labels work: you simply use a label and it gets its
    #: own ``intbv`` object.  Then when you use the ``label()``
    #: *directive* on that label the ``intbv`` gets updated with the
    #: actual current output address, and that value will be used to
    #: assemble the proper bit patterns in ``pass2()``.
    self.context = defaultdict(lambda: int2addr(0))

    self.context.update(self._instruction_namespace())
    self.context.update(self._directives())
    self.context.update((f.__name__, f) for f in (
        low,
        high,
        )
      )
    self.context['range'] = xrange
    if initial_context is not None:
      self.context.update(initial_context)

    #: Current output address of the assembly process.
    self.here = int2addr(0)

    #: Internal intermediate data structure.  This holds the output of
    #: the methods in the ``InstructionsMixin`` used to create the byte
    #: strings in ``pass2()``.
    self.data = {}

    #: Internal output data structure.  This holds the byte strings
    #: created in ``pass2()``.
    self.accumulator = {}

  def assemble(self, text):
    '''
    Assemble the string asm source code.

    :param text: Assembly source code.
    :type text: ``str``
    :rtype: ``None``
    '''
    exec text in self.context
    del self.context['__builtins__']
    self.pass2()

  def assemble_file(self, filename):
    '''
    Assemble asm source code from a named file.

    :param filename: File name of an assembly source code file.
    :type filename: ``str``
    :rtype: ``None``
    '''
    execfile(filename, self.context)
    del self.context['__builtins__']
    self.pass2()

  def pass2(self):
    '''
    Second pass of the assembly process.

    Once the asm source code has been assembled into the intermediate
    form (by ``assemble()`` or ``assemble_file()``) this method converts
    it into binary strings.

    :rtype: Mapping of addresses to strings (binary data) this data
       structure is the end result of the assembly process, just before
       emitting the strings in e.g. Intel HEX format for burning to a
       chip.
    '''
    accumulator = self.accumulator
    for addr in sorted(self.data):
      instruction = self.data[addr]
      op, args = instruction[0], instruction[1:]

      # Adjust addresses for relative ops.
      if op in ('rcall', 'rjmp', 'brne', 'breq', 'brlo', 'brcc', 'brsh'):
        args = self._adjust(op, args, ibv(int(addr, 16)))

      # see instruction in Amtel manual.
      elif op in ('clr', 'lsl'):
        args = args + args

      opf = self.ops.get(op, lambda *args: (0, args))
      n, data = opf(*args)

      if n <= 0:
        bindata = data
      elif n == 16:
        bindata = pack('H', data)
      else:
        bindata = pack('2H', data[32:16], data[16:])

##      if op in ('db', 'dw'):
##        log.debug(addr, 10 * ' ', op, len(data), 'bytes:', repr(data))
##      else:
##        try:
##          fdata = '%-10x' % (data,)
##        except TypeError:
##          log.debug(addr, 10 * '.', instruction, repr(data))
##        else:
##          log.debug(addr, fdata, instruction, repr(bindata))

      accumulator[addr] = bindata

    return accumulator

  def _name_of_address_thunk(self, thunk):
    for k, v in self.context.iteritems():
      if v is thunk:
        return k
    return '%#06x' % thunk

  def _get_here(self):
    addr = '%#06x' % (self.here,)
    assert addr not in self.data
    return addr

  def _name_or_addr(self, address):
    if isinstance(address, str):
      assert len(address) == 1, repr(address)
      address = ord(address)

    if isinstance(address, int):
      name = '%#06x' % address
      address = int2addr(address)
    else:
      assert isinstance(address, intbv), repr(address)
      name = self._name_of_address_thunk(address)
    return name, address

  def _adjust(self, op, args, addr):
    return (ibv(args[0] - addr - 1),)

  def to_hex(self, f):
    '''
    Convert the assembled machine code to Intel HEX file format.

    :param f: The HEX data will be written to this destination.
    :type f: filename or file-like object
    '''
    from intelhex import IntelHex
    ih = IntelHex()
    for addr, val in self.accumulator.iteritems():
      addr = int(addr, 16)
      ih.puts(addr, val)
    ih.write_hex_file(f)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser(description='Simple assembler for ATmega328P')
  parser.add_argument(
    '-x', '--hex',
    help='Write HEX output to this file. (Use - for stdout.)',
    )
  parser.add_argument('source', help='Source code file to assemble.')
  args = parser.parse_args()

  import m328P_def
  aa = AVRAssembly(m328P_def.defs)
  aa.assemble_file(args.source)
  if args.hex:
    if args.hex == '-':
      from sys import stdout
      f = stdout
    else:
      f = args.hex
    aa.to_hex(f)
  else:
    pprint.pprint(aa.data)
