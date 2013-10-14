class Context(object):

  def __init__(self, text, stack=[]):
    self.success = True
    self.stack = stack
    self.text = text
    self.pointer = 0

  def advance(self): self.pointer += 1
  def parse(self, *terms): C(*terms)(self)
  def current(self): return self.text[self.pointer]
  def push(self): self.stack.append(self.pointer)
  def fail(self): self.pointer = self.stack.pop()
  def okay(self): self.stack.pop()

  def __repr__(self):
    return '<Context %s %r, %i %r>' % (
      self.success, self.current(), self.pointer, self.stack)

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

H, h, e, l = map(make_char_tokenizer, 'Hhel')

Context('Hello World').parse(h, OR, H, e, l, l) ; print
Context('hello World').parse(h, OR, H, e, l, l) ; print
Context('Hello World').parse(C(h, OR, H), e, l, l) ; print

c = Context('hello World')
C(h, OR, H)(c)
C(e, l, l)(c)
