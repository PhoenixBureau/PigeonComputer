#
#    Copyright © 2021 Simon Forman
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
from io import StringIO


class MetaII(object):

  def __init__(self):
    self.reset()

  def reset(self):
    self.program = []
    self.labels = {}
    self.pos = 0
    self.outbuf = ""
    self.margin = 0
    self.gnlabel = 1
    self.switch = False
    self.PC = 0
    self.stack = [(False, -1), None, None]
    self.output = StringIO()
    self._indent = '    '
    self.indent = 0
    self.last = None
    self.error = self.end = False

  def runBEjsfn(self, rname):
    print('error in', rname)
    1/0

  # These are the "order codes" (assembly instructions) for the Meta II
  # metacompiler machine.

  def TST(self, string):
    '''
    Look for and consume the string in the input text, setting switch if
    found, otherwise consume nothing (but leading whitespace) and reset
    switch.  Strips all leading whitespace.
    '''
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

  def SET(self):
    '''
    Set switch.
    '''
    self.switch = True

  def CL(self, string):
    '''
    Copy literal to output buffer.
    '''
    self._out(string)

  def CI(self):
    '''
    Copy ``last`` buffer contents to output buffer.
    '''
    self._out(self.last)

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

  # Those are the order codes. The rest of these are support methods.

  def _left_trim_input(self):
    self.input = self.input.lstrip()

  def _out(self, s):
    self.output_buffer += s
