class Context(object):

  def __init__(self, text):
    self.success = True
    self.stack = []
    self.text = text
    self.pointer = 0

  def advance(self): self.pointer += 1
  def parse(self, *terms): self.push() ; C(*terms)(self)
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
  @deco_chk
  def c(context):
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

c = Context('Hello World')
c.parse(h, OR, H, e, l, l) ; print c ; print
c = Context('hello World')
c.parse(h, OR, H, e, l, l) ; print c ; print
c = Context('Hello World')
c.parse(C(h, OR, H), e, l, l) ; print c ; print
