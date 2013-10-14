'''

Each term examines the stack on entry. if false, the word exits immediately with false on the stack.



|| given a true value on the stack, exits the colon definition immediately with true on the stack.

&& given a false value on the stack, exits the colon definition immediately with false on the stack.

We assume that each "token" (terminal) is represented by a Forth word which scans the input stream and 
returns a success flag.

'''

class Context(object):

  def __init__(self, stream, stack=[]):
    self.success = True
    self.stack = stack
    self.stream = Stream(stream, True)

  def parse(self, *terms):
    C(*terms)(self)

  def __repr__(self):
    return '<Context %s %r>' % (self.success, self.stream.current)


class Stream(object):
  def __init__(self, thing, start=False):
    self.i = iter(thing)
    self._thing = thing
    self.current = None if not start else next(self.i)

  def next(self):
    it = self.current = next(self.i)
    return it


class PopFrame(Exception): pass


def OR(context):
  if context.success:
    raise PopFrame
  context.success = True


def C(*terms):
  def c(context):
    try:
      for term in terms:
        term(context)
    except PopFrame:
      pass
  return c


def deco_chk(f):
  return lambda context: f(context) if context.success else None


def make_char_tokenizer(char):
  @deco_chk
  def tok(context):
    print context, '=?=', char
    if context.stream.current != char:
      context.success = False
    else:
      context.stream.next()
  return tok


H = make_char_tokenizer('H')
h = make_char_tokenizer('h')
e = make_char_tokenizer('e')
l = make_char_tokenizer('l')


h = C(h, OR, H, e, l, l)
j = C(C(h, OR, H), e, l, l)

Context('Hello World').parse(h)
print
Context('hello World').parse(h)
print

Context('Hello World').parse(j)
print

c = Context('hello World')
C(h, OR, H)(c)
C(e, l, l)(c)


