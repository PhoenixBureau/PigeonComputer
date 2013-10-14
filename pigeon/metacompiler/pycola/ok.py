class Stream:

  def __init__(self, text):
    self.text = text
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
    if context.success:
      f(context)
  return chk

def chartok(char):
  @deco
  def tok(context):
    if context.stream.current == char:
      context.stream.advance()
    else:
      context.success = False
  return tok


context = Context('Hello world!')
H = chartok('H')
