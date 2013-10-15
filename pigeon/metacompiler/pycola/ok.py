from string import ascii_letters, digits, whitespace
import sys

class Context:
  def __init__(self, text):
    self.stream = iter(text)
    self.advance()
    self.success = True
  def advance(self):
    try:
      self.current = self.stream.next()
    except StopIteration:
      if not self.success:
        raise
  def __repr__(self):
    return '<Context %r %s >' % (self.current, self.success)

def deco(f):
  def chk(context):
    if context.success: f(context)
  return chk

def chartok(char):
  @deco
  def tok(context):
    if context.current == char:
      print >> sys.stderr, char, context
      context.advance()
    else:
      context.success = False
  return tok

def rangetok(start, stop):
  @deco
  def tok(context):
    if start <= context.current <= stop:
      print >> sys.stderr, start, '-', stop, context
      context.advance()
    else:
      context.success = False
  return tok

class PopFrame(Exception): pass

def OR(context):
  if context.success:
    raise PopFrame
  context.success = True

def seq(*terms):
  @deco
  def do_seq(context):
    try:
      for term in terms: term(context)
    except PopFrame:
      pass
  return do_seq

def kstar(term):
  @deco
  def kst(context):
    while context.success: term(context)
    context.success = True
  return kst

def parse(text, pattern):
  context = Context(text)
  pattern(context)
  return context


##alphabet = map(chartok, ascii_letters)
##numerals = map(chartok, digits)

blanc = [OR] * (len(whitespace) * 2 - 1)
blanc[::2] = map(chartok, whitespace) #Python is cool. ;)
blanc = seq(*blanc)
__ = kstar(blanc)

##_l = locals()
##for name, tokeneater in zip(ascii_letters, alphabet):
##  _l[name] = tokeneater
##for name, tokeneater in zip(digits, numerals):
##  _l['_' + name] = tokeneater
##del _l

lparen, rparen = chartok('('), chartok(')')
dot = chartok('.')
quote = chartok("'")
low = rangetok('a', 'z')
high = rangetok('A', 'Z')
letter = seq(low, OR, high)
digit = rangetok('0', '9')
number = seq(digit, kstar(digit))
anychar = kstar(seq(letter, OR, digit))
symbol = seq(letter, anychar)
string = seq(quote, anychar, quote)
term = seq(number, OR, symbol, OR, string)

@deco
def do_list(context):
  seq(
    lparen, __,
    kstar(seq(seq(term, OR, do_list), __)),
    rparen
    )(context)

little_language = seq(__, kstar(seq(seq(term, OR, do_list), __)), dot)

c = Context(" ( 123 a (bb c 34)) 34 '' ('Tuesday') .")
little_language(c)
print c
