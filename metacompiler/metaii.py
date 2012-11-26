'''
Python implementation of the Meta II compiler
'''
from StringIO import StringIO
from pprint import pformat


class MetaII(object):

  def __init__(self):
    self.program = []
    self.labels = {}

  def assemble(self, program_source):
    for line in program_source.splitlines(False):
      if not line or line.isspace():
        continue
      if line[0].isspace():
        self.assemble_line(*line.split(None, 1))
      else:
        label = line.strip()
        self.labels[label] = len(self.program)
      
  def assemble_line(self, op, arg=''):
    f = getattr(self, op)
    arg = (arg,) if arg else ()
    self.program.append((f, arg))

  def compile(self, input_text):
    self.switch = False
    self.PC = 0
    self.stack = [(False, -1), None, None]
    self.input = input_text
    self.output = StringIO()
    self.output_buffer = '\t'
    self.last = None
    self.error = self.end = False
    self.q = label_generator().next
    while not (self.error or self.end):
      op, args = self.program[self.PC]
      op(*args)
      self.PC += 1
    return self.output.getvalue()

  def ADR(self, ident):
    self.PC = self.labels[ident] - 1

  def TST(self, string):
    string = string[1:-1]
    self._left_trim_input()
    self.switch = self.input.startswith(string)
    if self.switch:
      self.last = string
      self.input = self.input[len(string):]

  def ID(self):
    self._left_trim_input()
    I = self.input
    if not I[0].isalpha():
      self.switch = False
      return
    n = 1
    while I[n].isalnum():
      n += 1
    self.last, self.input, self.switch = I[:n], I[n:], True

  def NUM(self):
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
    addr = self.labels[addr]
    push_call_frame(self.stack, self.PC)
    self.PC = addr - 1

  def R(self):
    self.PC = pop_call_frame(self.stack)
    if self.PC == -1:
      self.end = True

  def SET(self):
    self.switch = True

  def B(self, addr):
    self.PC = self.labels[addr] - 1

  def BT(self, addr):
    if self.switch:
      self.PC = self.labels[addr] - 1

  def BF(self, addr):
    if not self.switch:
      self.PC = self.labels[addr] - 1

  def BE(self):
    if not self.switch:
      self.error = True

  def CL(self, string):
    self._out(string[1:-1])

  def CI(self):
    self._out(self.last)

  def GN1(self):
    cell = self.stack[-1]
    if not cell:
      cell = self.stack[-1] = self.q()
    self._out(cell)
    
  def GN2(self):
    cell = self.stack[-2]
    if not cell:
      cell = self.stack[-2] = self.q()
    self._out(cell)

  def LB(self):
    self.output_buffer = self.output_buffer.lstrip()

  def OUT(self):
    print >> self.output, self.output_buffer.rstrip()
    self.output_buffer = '\t'

  def END(self):
    pass

  def _left_trim_input(self):
    self.input = self.input.lstrip()

  def _out(self, s):
    self.output_buffer += s

  def _get_first_word(self, default=''):
    i = self.input.split(None, 1)
    if len(i) == 1:
      return i[0], default
    return i

  def info(self):
    print 'Stack:', pformat(self.stack)
    print 'last:', repr(self.last), 'switch:', self.switch
    print 'input:', repr(self.input[:20])
    print 'PC:', self.PC,
    op, args = self.program[self.PC]
    L = self._labels_for_address(self.PC)
    if L:
      print L, ':',
    print op.__name__ + str(args)

  def print_program(self):
    for n, (f, a) in enumerate(self.program):
      L = self._labels_for_address(n)
      if L:
        print L, ':'
      print '    %3i %3s %r' % (n, f.__name__, a)

  def _labels_for_address(self, addr):
    return ' '.join(
      k for k, v in self.labels.iteritems()
      if v == addr
      )


def push_call_frame(stack, addr):
  blank_already = stack[-2] is stack[-1] is None
  if blank_already:
    stack.append(None)
  else:
    stack.extend((None, None, None))
  stack[-3] = blank_already, addr


def pop_call_frame(stack):
  were_blank, return_address = stack[-3]
  if were_blank:
    stack[-3:] = [None, None]
  else:
    del stack[-3:]
  return return_address


def label_generator():
  n = 1
  while True:
    yield 'L' + str(n)
    n += 1


if __name__ == '__main__':
  metaii_source = open('metaii.asm').read()
  metaii_description = open('metaii.metaii').read()
  m2 = MetaII()
  m2.assemble(metaii_source)
  new_source = m2.compile(metaii_description)
  print new_source
