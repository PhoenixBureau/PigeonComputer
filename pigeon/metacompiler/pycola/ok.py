import sys

class Stream:
  def __init__(self, text):
    self.i = iter(text)
    self.advance()
  def advance(self):
    self.current = self.i.next()

class Context:
  def __init__(self, text):
    self.stream = Stream(text)
    self.success = True
  def __repr__(self):
    return '<Context %r %s >' % (self.stream.current, self.success)

def deco(f):
  def chk(context):
    if context.success: f(context)
  return chk

def chartok(char):
  @deco
  def tok(context):
    print >> sys.stderr, char, context
    if context.stream.current == char:
      context.stream.advance()
    else:
      context.success = False
  return tok

class PopFrame(Exception): pass

def OR(context):
  if context.success: raise PopFrame
  context.success = True

def seq(*terms):
  @deco
  def do_seq(context):
    try:
      for term in terms: term(context)
    except PopFrame:
      pass
  return do_seq

context = Context('Hello world!')
H = chartok('H')
h = chartok('h')
e = chartok('e')
l = chartok('l')
h2 = seq(h, OR, H, e, l, l)
h3 = seq(H, OR, h, e, l, l)
h4 = seq(seq(h, OR, H), e, l, l)
