from co import bootstrap, send, addMethod, lookup
from la import setUpTransformEngine


#########################################################################
##  COLA Machinery


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)


#########################################################################
##  Abstract Syntax Tree


def allocate(vt):
  return send(vt, 'allocate')

def delegated(vt):
  return send(vt, 'delegated')


def make_kind(kind):
  return send(allocate(symbol_vt), 'setName', kind)
def make_ast(KIND, value):
  return send(allocate(ast_vt), 'init', KIND, value)

def name_of_symbol_of(ast):
  return send(send(ast, 'typeOf'), 'getName')


SYMBOL = make_kind('symbol')
LITERAL = make_kind('literal')
LIST = make_kind('list')


def symbol(name):
  return make_ast(SYMBOL, name)

def literal(value):
  return make_ast(LITERAL, value)

def list_(*values):
  return make_ast(LIST, list(values))


#########################################################################
##  Parser


def advance(context):
  send(context, 'collect')
  stream = send(context, 'lookup', 'stream')
  try:
    char = stream.next()
  except StopIteration:
    if not send(context, 'lookup', 'success'):
      raise
    else:
      send(context, 'addMethod', 'current', '')
  else:
    send(context, 'addMethod', 'current', char)


def collect(context):
  if send(context, 'lookup', 'collecting'):
    basket = send(context, 'lookup', 'basket')
    current = send(context, 'lookup', 'current')
    basket.append(current)


def push(context, term):
  send(context, 'lookup', 'current_frame').append(term)


def start_frame(context):
  frame_stack = send(context, 'lookup', 'frame_stack')
  current_frame = send(context, 'lookup', 'current_frame')
  frame_stack.append(current_frame)
  send(context, 'addMethod', 'current_frame', [])


def finish_frame(context):
  frame_stack = send(context, 'lookup', 'frame_stack')
  current_frame = send(context, 'lookup', 'current_frame')
  frame_stack[-1].append(list_(*current_frame))
  send(context, 'addMethod', 'current_frame', frame_stack.pop())


context_vt = delegated(vtvt)
for method in (advance, collect, push, start_frame, finish_frame):
  send(context_vt, 'addMethod', method.__name__, method)


def makeContext(text):
  context = allocate(context_vt)
  context.data = {}
  send(context, 'addMethod', 'context', context)
  send(context, 'addMethod', 'stream', iter(text))
  send(context, 'addMethod', 'basket', [])
  send(context, 'addMethod', 'collecting', False)
  send(context, 'addMethod', 'success', True)
  send(context, 'addMethod', 'frame_stack', [])
  send(context, 'addMethod', 'current_frame', [])
  send(context, 'advance')
  return context


def deco(f):
  def chk(context):
    if send(context, 'lookup', 'success'):
      f(context)
  return chk


def chartok(char):
  @deco
  def tok(context):
    if send(context, 'lookup', 'current') == char:
      send(context, 'advance')
    else:
      send(context, 'addMethod', 'success', False)
  return tok


def rangetok(start, stop):
  @deco
  def tok(context):
    if start <= send(context, 'lookup', 'current') <= stop:
      send(context, 'advance')
    else:
      send(context, 'addMethod', 'success', False)
  return tok


class PopFrame(Exception):
  pass


def OR(context):
  if send(context, 'lookup', 'success'):
    raise PopFrame
  send(context, 'addMethod', 'success', True)


def seq(*terms):
  @deco
  def do_seq(context):
    try:
      for term in terms:
        term(context)
    except PopFrame:
      pass
  return do_seq


def kstar(term):
  @deco
  def kst(context):
    while send(context, 'lookup', 'success'):
      term(context)
    send(context, 'addMethod', 'success', True)
  return kst


def capture(f, post_process=eval):
  @deco
  def bracket(context):
    send(context, 'addMethod', 'collecting', True)
    b = send(context, 'lookup', 'basket')
    f(context)
    if send(context, 'lookup', 'success'):
      send(context, 'push', post_process(''.join(b)))
    del b[:]
    send(context, 'addMethod', 'collecting', False)
  return bracket


@deco
def start_frame(context):
  send(context, 'start_frame')


@deco
def finish_frame(context):
  send(context, 'finish_frame')


#########################################################################
##  Little Language


from string import whitespace
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
number = capture(seq(digit, kstar(digit)), lambda i: literal(int(i)))
alnum = seq(letter, OR, digit)
anychar = seq(alnum, OR, blanc)
symbol = capture(seq(letter, kstar(alnum)), symbol)
string = capture(seq(quote, kstar(anychar), quote), lambda i: literal(eval(i)))
term = seq(number, OR, symbol, OR, string)

@deco
def do_list(context):
  for it in (
    lparen, start_frame, __,
    kstar(seq(term, __, OR, do_list)),
    rparen, finish_frame, __
    ):
    it(context)


little_language = seq(__, kstar(do_list), dot)


#########################################################################
##  LISP-ish Evaluator


def evaluate(ast, context):
  sname = name_of_symbol_of(ast)
  if sname == 'symbol':
    try:
      return send(context, 'lookup', ast.data)
    except:
      return str(ast.data) + '?'

  if sname == 'literal':
    return ast.data

  first, rest = ast.data[0], ast.data[1:]
  sname = name_of_symbol_of(first)
  if sname == 'symbol':
    if first.data == 'define':
      define(rest, context)
      return
    if first.data == 'lambda':
      return make_lambda_ast(rest, context)

  exp = tuple(evaluate(it, context) for it in ast.data)
  if callable(exp[0]):
    return exp[0](*exp[1:])
  return exp


def define((var, exp), context):
  send(context, 'addMethod', var.data, evaluate(exp, context))


def make_lambda_ast((variables, exp), context):
  variables = tuple(v.data for v in variables.data)
  exp = list_(*exp.data)
  def inner(*args):
    new_context = send(context, 'delegated')
    for k, v in zip(variables, args):
      send(new_context, 'addMethod', k, v)
    return evaluate(exp, new_context)
  return inner


def evaluate_list(ast, context):
  result = evaluate(ast, context)
  if result is not None:
    print '<', result, '>'


#########################################################################
##  Simple AST Pretty Printer


# We can also use machinery like this to walk the AST and print a
# representation.

def emit_lit(ast, context):
  print ' ' * context.indent, repr(ast.data)

def emit_word(ast, context):
  print ' ' * context.indent, '< %s >' % (ast.data,)

def emit_seq(ast, context):
  context.indent += 3
  print ' ' * context.indent, '/----\\'
  for item in ast.data:
    send(item, 'eval', context)
  print ' ' * context.indent, '\\____/'
  context.indent -= 3


def prep_emit_context(context):
  send(context, 'addMethod', 'literal', emit_lit)
  send(context, 'addMethod', 'symbol', emit_word)
  send(context, 'addMethod', 'list', emit_seq)
  context.indent = 0


#########################################################################
##  Put it all together and you haxz a neat little environment.


if __name__ == '__main__':
  from pprint import pprint

  c = makeContext('''

  (12) ( 3 'fo ur' ) ( 5 (6 (7) bo )bo)

  (define p (divide 1 1000000000))
  (define pi (multiply 3141592653 p))

  (define area (lambda (r) (multiply pi (multiply r r))))

  ( area 23 nic )

  .''')

  little_language(c)

  del c.data['context'] ; print ; print ; pprint(c.data) ; print

  prep_emit_context(c)
  for it in c.data['current_frame']:
    send(it, 'eval', c)
    print
  print

  send(c, 'addMethod', 'multiply', lambda x, y: y * x)
  send(c, 'addMethod', 'divide', lambda x, y: x / float(y))

  send(c, 'addMethod', 'list', evaluate_list)

  for it in c.data['current_frame']:
    send(it, 'eval', c)
    print
  print
