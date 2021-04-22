#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © 2012 Simon Forman
#
#    This file is part of Pigeon Computer.
#
#    Pigeon Computer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pigeon Computer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pigeon Computer.  If not, see <http://www.gnu.org/licenses/>.
#
'''
==========================================
Meta II Meta-Compiler (Python Engine)
==========================================

This is a Python implementation of Val Shorre's `Meta II metacompiler`_.

It is just the engine, the Meta-II machine, *not* a self-regenerating
metacompiler.  It *does* run the Meta-II assembly code and can scan the
Meta-II compiler description and (re-)compile that assembly code.

This engine can be used to play with metacompilers and generate all sorts
of cool and interesting things (see the Bayfront Technologies
`Metacompilers Tutorial`_.)  We're going to use it to target the Pigeon
Assembler's source format.

We can compile descriptions of high-level programming language constructs
into assembly code and then use the assembler to generate HEX files to
load on our chips, giving us a simple but powerful *toolchain* for
developing code for our micro-controllers.


.. _Meta II metacompiler: http://en.wikipedia.org/wiki/META_II

.. _Metacompilers Tutorial: http://www.bayfronttechnologies.com/mc_tutorial.html

'''
from io import StringIO


class MetaII(object):
  '''
  Implementation of Val Shorre's Meta II metacompiler.
  (see http://en.wikipedia.org/wiki/META_II)

  usage: metaii.py [-h] [-p PROGRAM] source

  positional arguments::

     source                Source code file to compile.

  optional arguments::

     -h, --help            show this help message and exit

     -p PROGRAM, --program PROGRAM
                          Assembly file to use for compiler (default:
                          metaii.asm).
  '''
  def __init__(self):
    self.program = []
    self.labels = {}

  def assemble(self, program_source):
    '''
    Assemble the provided Meta II assembly source text and become the
    machine (compiler) defined by that program.
    '''
    for line in program_source.splitlines(False):
      if not line or line.isspace():
        continue
      if line[0].isspace():
        self.program.append(self.assemble_line(*line.split(None, 1)))
      else:
        label = line.strip()
        self.labels[label] = len(self.program) - 1

  def assemble_line(self, op, arg=None):
    '''
    Used by the ``assemble()`` method to process each non-label input
    line in the assembly source text.
    '''
    f = getattr(self, op)
    arg = (arg,) if arg is not None else ()
    return f, arg

  def compile(self, input_text):
    '''
    Once a compiler assembly source text has been assembled (using the
    ``assemble()`` method) you can pass source code in the compiler's
    language to this method to compile it.

    :param input_text: Source code in the language recognized by the
       machine passed to the ``assemble()`` method.
    :type input_text: ``str``
    :rtype: ``str``
    '''
    self.switch = False
    self.PC = 0
    self.stack = [(False, -1), None, None]
    self.input = input_text
    self.output = StringIO()
    self.output_buffer = ''
    self._indent = '    '
    self.indent = 0
    self.last = None
    self.error = self.end = False
    self.q = label_generator().__next__
    while not (self.error or self.end):
      op, args = self.program[self.PC]
      op(*args)
      self.PC += 1
    return self.output.getvalue()

  # These are the "order codes" (assembly instructions) for the Meta II
  # metacompiler machine.

  def ADR(self, ident):
    '''
    Set PC to the given label/address.
    '''
    self.PC = self.labels[ident]

  def TST(self, string):
    '''
    Look for and consume the string in the input text, setting switch if
    found, otherwise consume nothing (but leading whitespace) and reset
    switch.  Strips all leading whitespace.
    '''
    string = string[1:-1]
    self._left_trim_input()
    self.switch = self.input.startswith(string)
    if self.switch:
      self.last = string
      self.input = self.input[len(string):]

  def ID(self):
    '''
    Strip all leading whitespace and scan for an identifier.  If found
    consume it, store it in the ``last`` buffer and set switch, otherwise
    reset the switch.
    '''
    self._left_trim_input()
    I = self.input
    if not I[0].isalpha() or I[0] == '_':
      self.switch = False
      return
    n = 1
    while I[n].isalnum() or I[n] == '_':
      n += 1
    self.last, self.input, self.switch = I[:n], I[n:], True

  def NUM(self):
    '''
    Strip all leading whitespace and scan for a number.  If found consume
    it, store it in the ``last`` buffer and set switch, otherwise reset
    the switch.
    '''
    self._left_trim_input()
    I, n = self.input, 0
    while I[n] in set('0123456789.'):
      n += 1
    num, rest = I[:n], I[n:]
    self.switch = n and num[0].isdigit() and num[-1].isdigit()
    if self.switch and n > 3:
      self.switch = not any(
        num[n + 1] == '.'
        for n in range(1, len(num) - 2)
        if num[n] == '.'
        )
    if self.switch:
      self.last = num
      self.input = rest

  def SR(self):
    '''
    Strip all leading whitespace and scan for a string (enclosed in
    single quotes.)  If found consume it, store it in the ``last`` buffer
    and set switch, otherwise reset the switch.
    '''
    self._left_trim_input()
    I = self.input
    if I[0] != "'":
      self.switch = False
      return
    n, L = 1, len(I)
    while n < L:
      if I[n] == "'":
        n += 1
        self.last, self.input, self.switch = I[:n], I[n:], True
        break
      n += 1
    else:
      self.switch = False

  def CLL(self, addr):
    '''
    Call the subroutine at ``addr``.
    '''
    self._push_call_frame()
    self.PC = self.labels[addr]

  def R(self):
    '''
    Return from a subroutine.
    '''
    self.PC = self._pop_call_frame()
    if self.PC == -1:
      self.end = True

  def SET(self):
    '''
    Set switch.
    '''
    self.switch = True

  def B(self, addr):
    '''
    Unconditional branch to ``addr``.
    '''
    self.PC = self.labels[addr]

  def BT(self, addr):
    '''
    Branch to ``addr`` if switch is set.
    '''
    if self.switch:
      self.PC = self.labels[addr]

  def BF(self, addr):
    '''
    Branch to ``addr`` if switch is clear.
    '''
    if not self.switch:
      self.PC = self.labels[addr]

  def BE(self):
    '''
    Branch to error. Terminates compilation and (by default) prints a bit
    of debugging information.
    '''
    if not self.switch:
      self.error = True

  def CL(self, string):
    '''
    Copy literal to output buffer.
    '''
    self._out(string[1:-1])

  def CI(self):
    '''
    Copy ``last`` buffer contents to output buffer.
    '''
    self._out(self.last)

  def GN(self):
    '''
    "If the label 1 cell in the top stackframe is blank,
    generate a unique number and save it in the label 1 cell.
    In either case output the label."
    http://www.bayfronttechnologies.com/mc_tutorial.html#s07
    '''
    cell = self.stack[-1]
    if not cell:
      cell = self.stack[-1] = self.q()
    self._out(cell)

  def LB(self):
    '''
    "Move to output column 1."
    '''
    self.output_buffer = ''

  def TB(self):
    '''
    "Move to the next tab stop."
    '''
    self.output_buffer += self._indent

  def LMI(self):
    '''
    "Increase the left margin, indenting block."
    '''
    self.indent += 1

  def LMD(self):
    '''
    "Decrease the left margin, indenting block."
    '''
    self.indent -= 1

  def NL(self):
    '''
    "Flush output buffer with ending newline and move to left margin."
    '''
    print(self.output_buffer.rstrip(), file=self.output)
    self.output_buffer = self._indent * self.indent

  def END(self):
    '''
    Terminate compilation normally.
    '''
    pass

  # Those are the order codes. The rest of these are support methods.

  def _left_trim_input(self):
    self.input = self.input.lstrip()

  def _out(self, s):
    self.output_buffer += s

  def _push_call_frame(self):
    blank_already = self.stack[-2] is self.stack[-1] is None
    if blank_already:
      self.stack.append(None)
    else:
      self.stack.extend((None, None, None))
    self.stack[-3] = blank_already, self.PC

  def _pop_call_frame(self):
    were_blank, return_address = self.stack[-3]
    if were_blank:
      self.stack[-3:] = [None, None]
    else:
      del self.stack[-3:]
    return return_address

  # Some debugging/introspection methods.  (Not strictly needed.)

  def info(self):
    '''
    Print out some useful information about the current state of the
    assembler/compiler.  Used for debugging and after errors to report,
    uh, errors.
    '''
    from pprint import pformat
    print('Stack:', pformat(self.stack))
    print('last:', repr(self.last), 'switch:', self.switch)
    print('input:', repr(self.input[:20]))
    print('PC:', self.PC, end=' ')
    op, args = self.program[self.PC]
    L = self._labels_for_address(self.PC)
    if L:
      print(L, ':', end=' ')
    print(op.__name__ + str(args))

  def print_program(self):
    '''
    Print out a dump of the assembled compiler machine's program.  Used
    for debugging.
    '''
    for n, (f, a) in enumerate(self.program):
      L = self._labels_for_address(n)
      if L:
        print(L, ':')
      print('    %3i %3s %r' % (n, f.__name__, a))

  def _labels_for_address(self, addr):
    return ' '.join(k for k, v in self.labels.items() if v == addr)


def label_generator():
  '''
  Generator of string label numbers: '1', '2', '3', ...
  '''
  n = 1
  while True:
    yield str(n)
    n += 1


def comp(source, machine):
  m2 = MetaII()
  m2.assemble(machine)
  return m2.compile(source)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser(description=__doc__)
  parser.add_argument(
    '-p', '--program',
    default='metaii.asm',
    help='Assembly file to use for compiler (default: %(default)s).',
    )
  parser.add_argument('source', help='Source code file to compile.')
  args = parser.parse_args()

  metaii_asm = open(args.program).read()
  metaii_description = open(args.source).read()

  m2 = MetaII()
  m2.assemble(metaii_asm)
  new_asm = m2.compile(metaii_description)
  print(new_asm)
  if m2.error:
    m2.info()
#  print new_asm.rstrip() == metaii_asm.rstrip()
