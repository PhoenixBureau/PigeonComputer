'''

Each term examines the stack on entry. if false, the word exits immediately with false on the stack.



|| given a true value on the stack, exits the colon definition immediately with true on the stack.

&& given a false value on the stack, exits the colon definition immediately with false on the stack.

We assume that each "token" (terminal) is represented by a Forth word which scans the input stream and 
returns a success flag.

'''

class Context(object):

  def __init__(self, text, stack=[]):
    self.success = True
    self.stack = stack
    self.text = text
    self.pointer = 0

  def advance(self):
    self.pointer += 1

  def parse(self, *terms):
    C(*terms)(self)

  def current(self):
    return self.text[self.pointer]

  def push(self):
    self.stack.append(self.pointer)

  def fail(self):
    self.pointer = self.stack.pop()

  def okay(self):
    self.stack.pop()

  def __repr__(self):
    return '<Context %s %r, %i>' % (self.success, self.current(), self.pointer)


class PopFrame(Exception): pass


def OR(context):
  if context.success:
    context.okay()
    raise PopFrame
  context.fail()
  context.success = True


def C(*terms):
  def c(context):
    context.push()
    try:
      for term in terms:
        term(context)
    except PopFrame:
      pass
  return c


def deco_chk(f):
  def chk(context):
    if context.success:
      context.push()
      f(context)
      if not context.success:
        context.fail()
      else:
        context.okay()
  return chk



def make_char_tokenizer(char):
  @deco_chk
  def tok(context):
    print context, '=?=', char
    if context.current() != char:
      context.success = False
    else:
      context.advance()
  return tok


H = make_char_tokenizer('H')
h = make_char_tokenizer('h')
e = make_char_tokenizer('e')
l = make_char_tokenizer('l')


h = C(h, OR, H, e, l, l)
j = C(C(h, OR, H), e, l, l)

Context('Hello World').parse(h)
print
c = Context('hello World')
c.parse(h)
print

Context('Hello World').parse(j)
print

c = Context('hello World')
C(h, OR, H)(c)
C(e, l, l)(c)


