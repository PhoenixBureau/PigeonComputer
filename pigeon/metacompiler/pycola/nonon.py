from co import bootstrap, send
from la import setUpTransformEngine
from metaii import comp


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)


#########################################################################
##  Simple Syntax to AST                                               ##
#########################################################################


# Helper functions.
def allocate(vt): return send(vt, 'allocate')
def make_kind(kind): return send(allocate(symbol_vt), 'setName', kind)
def make_ast(KIND, value): return send(allocate(ast_vt), 'init', KIND, value)
def name_of_symbol_of(ast): return send(send(ast, 'typeOf'), 'getName')


# Some AST symbol types.
SYMBOL = make_kind('symbol')
LITERAL = make_kind('literal')
LIST = make_kind('list')


# Helper functions to generate AST for the simple compiler below.
def symbol(name): return make_ast(SYMBOL, name)
def literal(value): return make_ast(LITERAL, value)
def list_(*values): return make_ast(LIST, list(values))


# META-II compiler for a simple s-expression language, it generates AST
# objects using the helper functions above when evaluated.
cola_machine = comp(r'''

  .SYNTAX PROGRAM

  PROGRAM = .OUT('(') args .OUT(')') '.' ;

  args = $ term ;

  term = ( list | literal | symbol ) .OUT(', ') ;

  list = '(' .OUT('list_(') args ')' .OUT(')') ;

  literal = ( .STRING | .NUMBER ) .OUT('literal('*')') ;

  symbol = .ID .OUT('symbol("'*'")') ;

  .END

''', open('metaii.asm').read())


#########################################################################
#########################################################################
#########################################################################


# Once we have AST we can use this LISP-like machinery to evaluate it.


def evaluate(ast, context):
  sname = name_of_symbol_of(ast)

  if sname == 'symbol':
    try: return send(context, 'lookup', ast.data)
    except: return str(ast.data) + '?'

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
  return


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


eval_context = send(object_vt, 'delegated')
send(eval_context, 'addMethod', 'list', evaluate_list)


#########################################################################
#########################################################################
#########################################################################


# We can also use machinery like this to walk the AST and print a
# representation.

def emit_lit(ast, context):
  print ' ' * context.indent, repr(ast.data)

def emit_word(ast, context):
  print ' ' * context.indent, '< %s >' % (ast.data,)

def eval_seq(ast, context):
  context.indent += 3
  print ' ' * context.indent, '/----\\'
  for item in ast.data:
    send(item, 'eval', context)
  print ' ' * context.indent, '\\____/'
  context.indent -= 3


print_context = send(object_vt, 'delegated')
send(print_context, 'addMethod', 'literal', emit_lit)
send(print_context, 'addMethod', 'symbol', emit_word)
send(print_context, 'addMethod', 'list', eval_seq)
print_context.indent = 0


#########################################################################
#########################################################################
#########################################################################


if __name__ == '__main__':
  from pprint import pprint

  send(eval_context, 'addMethod', 'multiply', lambda x, y: y * x)
  send(eval_context, 'addMethod', 'allocate', allocate)
  send(eval_context, 'addMethod', 'make_kind', make_kind)
  send(eval_context, 'addMethod', 'make_ast', make_ast)
  send(eval_context, 'addMethod', 'name_of_symbol_of', name_of_symbol_of)

  send(eval_context, 'addMethod',
       'eval_ast', lambda ast: evaluate_list(ast, eval_context)
       )

  body = comp('''

  ( define SYMBOL ( make_kind 'symbol' ) )
  ( define LITERAL ( make_kind 'literal' ) )
  ( define LIST ( make_kind 'list' ) )

  ( define symbol ( lambda (name) ( make_ast SYMBOL name ) ) )
  ( define literal ( lambda (value) ( make_ast LITERAL value ) ) )
  ( define list_ ( lambda (values) ( make_ast LIST values ) ) )

  ( define it ( list_ (
    ( symbol Larry )
    ( literal 23 )
    ( symbol Barry )
  )))

  ( eval_ast it )
  ( eval_ast ( symbol Bob ) )

  (define a 1)(define b Larry)
  (a b)

  (bill 23)

   (define area (lambda (r) (multiply 3.141592653 (multiply r r))))
   ( area 23 nic )
   ( 12 'neato' )
  .
  ''', cola_machine)

  ast = eval(body)

  print body
  print

  pprint(ast)
  print

  for ast_ in ast:
    send(ast_, 'eval', print_context)
    print

  print

  print 'Evaluating...' ; print
  for ast_ in ast:
    send(ast_, 'eval', eval_context)
