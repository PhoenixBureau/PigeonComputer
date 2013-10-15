from string import whitespace
import sys
from nonon import (
  symbol as SYM,
  literal as LIT,
  list_ as LIST,
  send,
  object_vt,
  print_context,
  eval_context,
  )


class Context:

  def __init__(self, text, context=None):
    self.stream = iter(text)
    self.advance()
    self.success = True
    self.current_frame = []
    self.frame_stack = []
    if context is None:
      context = send(object_vt, 'delegated')
    else:
      context = send(context, 'delegated')
    send(context, 'addMethod', 'compiler', self)
    send(context, 'addMethod', 'context', context)
    self.context = context

  def advance(self):
    self.collect()
    try:
      self.current = self.stream.next()
    except StopIteration:
      if not self.success:
        raise

  def collect(self):
    if hasattr(self, 'basket'):
      self.basket.append(self.current)

  def push(self, term):
    self.current_frame.append(term)

  def start_frame(self):
    self.frame_stack.append(self.current_frame)
    self.current_frame = []

  def finish_frame(self):
    self.frame_stack[-1].append(LIST(*self.current_frame))
    self.current_frame = self.frame_stack.pop()

  def finish_send(self):
    f = self.current_frame
    recipient, message, args = f[0].data, f[1].data, f[2:]
    print recipient, message, args
    recipient = send(self.context, 'lookup', recipient)
    result = send(recipient, message, *args)
    if result is not None:
      self.frame_stack[-1].append(result)
    self.current_frame = self.frame_stack.pop()
    

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
      context.advance()
    else:
      context.success = False
  return tok


def rangetok(start, stop):
  @deco
  def tok(context):
    if start <= context.current <= stop:
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


def capture(f, post_process=eval):
  @deco
  def bracket(context):
    b = context.basket = []
    f(context)
    if context.success:
      context.push(post_process(''.join(b)))
    del context.basket
  return bracket


@deco
def start_frame(context):
  context.start_frame()


@deco
def finish_frame(context):
  context.finish_frame()


@deco
def finish_send(context):
  context.finish_send()


blanc = [OR] * (len(whitespace) * 2 - 1)
blanc[::2] = map(chartok, whitespace) #Python is cool. ;)
blanc = seq(*blanc)
__ = kstar(blanc)
lparen, rparen = chartok('('), chartok(')')
lbrack, rbrack = chartok('['), chartok(']')
dot = chartok('.')
quote = chartok("'")
low = rangetok('a', 'z')
high = rangetok('A', 'Z')
letter = seq(low, OR, high)
digit = rangetok('0', '9')
number = capture(seq(digit, kstar(digit)), lambda i: LIT(int(i)))
anychar = kstar(seq(letter, OR, digit))
symbol = capture(seq(letter, anychar), SYM)
string = capture(seq(quote, anychar, quote), lambda i: LIT(eval(i)))
term = seq(number, OR, symbol, OR, string)
@deco
def do_list(context):
  for it in (
    lparen,
    start_frame,
    __,
    kstar(seq(term, __, OR, do_list, OR, do_send)),
    rparen,
    finish_frame,
    __
    ):
    it(context)

immediate_number = capture(seq(digit, kstar(digit)), int)
immediate_string = capture(seq(quote, anychar, quote))
immediate_term = seq(immediate_number, OR, symbol, OR, immediate_string)

@deco
def do_send(context):
  for it in (
    lbrack,
    start_frame,
    __,
    symbol, __,
    symbol, __,
    kstar(seq(immediate_term, __, OR, do_send)),
    rbrack,
    finish_send,
    __
    ):
    it(context)


little_language = seq(__, kstar(seq(do_list, OR, do_send)), dot)


if __name__ == '__main__':
  source = '''

     ( 123 a (bb c 34 ) )  ('Tuesday')

     [ context addMethod 'twentythree' 23 ]
     ( twentythree )
     ( ooo [ context addMethod 'g' [context lookup 'twentythree'] ])

     (define p (divide 1 1000000000))
     (define pi (multiply 3141592653 p))
     (pi p)
     (define area (lambda (r) (multiply pi (multiply r r))))
     ( area 23 nic )

     ( 12 'neato' )

  .'''

  c = Context(source, eval_context)

  little_language(c)
  print
  print c
  print c.context.data.keys()
  print

  for it in c.current_frame:
    send(it, 'eval', print_context)
    print
  print

  c = Context(source, eval_context)
  print 'Parsing...' ; print
  little_language(c)
  print 'Evaluating...' ; print
  for it in c.current_frame:
    send(it, 'eval', c.context)
  print

  send(eval_context, 'addMethod', 'multiply', lambda x, y: y * x)
  send(eval_context, 'addMethod', 'divide', lambda x, y: x / float(y))
  print 'Evaluating...' ; print
  for it in c.current_frame:
    send(it, 'eval', c.context)
  print
  print c.context.data.keys()
