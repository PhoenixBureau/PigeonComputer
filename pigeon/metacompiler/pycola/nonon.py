from pprint import pprint
from co import bootstrap, send
from la import setUpTransformEngine
from metaii import comp


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)

# Helper functions.
def allocate(vt): return send(vt, 'allocate')
def make_kind(kind): return send(allocate(symbol_vt), 'setName', kind)
def make_ast(KIND, value): return send(allocate(ast_vt), 'init', KIND, value)


# Some AST symbol types.
SYMBOL = make_kind('symbol')
LITERAL = make_kind('literal')
LIST = make_kind('list')


# Helper functions to generate AST for the simple "compiler" below.
def symbol(name): return make_ast(SYMBOL, name)
def literal(value): return make_ast(LITERAL, value)
def list_(*values): return make_ast(LIST, list(values))


# META-II source for a simple s-expression language, it generates AST
# objects using the helper functions above when evaluated.
cola_metaii = r'''

  .SYNTAX PROGRAM

  PROGRAM = .OUT('(') args .OUT(')') '.' ;

  args = $ term ;

  term = ( list | literal | symbol ) .OUT(', ') ;

  list = '(' .OUT('list_(') args ')' .OUT(')') ;

  literal = ( .STRING | .NUMBER ) .OUT('literal('*')') ;

  symbol = .ID .OUT('symbol("'*'")') ;

  .END

'''


# Once we have the AST we can use this LISP-like machinery to evaluate it.

def name_of_symbol_of(ast):
  return send(send(ast, 'typeOf'), 'getName')

def evaluate(ast, context):
  sname = name_of_symbol_of(ast)

  if sname == 'symbol':
    try:
      return send(context, 'lookup', ast.data)
    except:
      return ast.data

  if sname == 'literal':
    return ast.data

  first, rest = ast.data[0], ast.data[1:]
  sname = name_of_symbol_of(first)

  if sname == 'symbol':

    if first.data == 'define':
      var, exp = rest
      var = var.data
      value = evaluate(exp, context)
      send(context, 'addMethod', var, value)
      return

    elif first.data == 'lambda':
      return make_lambda_ast(rest, context)

  exp = tuple(evaluate(it, context) for it in ast.data)
  if callable(exp[0]):
    return exp[0](*exp[1:])

  return exp


def make_lambda_ast(rest, context):
  variables, exp = rest
  variables = tuple(v.data for v in variables.data)
  exp = list_(*exp.data)

  def inner(*args):
    new_context = send(context, 'delegated')
    for k, v in zip(variables, args):
      send(new_context, 'addMethod', k, v)
    return evaluate(exp, new_context)

  return inner


source = '''
(define a 1)
(a)

 (define area (lambda (r) (m 3.141592653 (multiply r r))))
 ( area cage nic )
 ( 12 'neato' )
.
'''

cola_machine = comp(cola_metaii, open('metaii.asm').read())
body = comp(source, cola_machine)
print body
print


ast = eval(body)
pprint(ast)
print


context = send(object_vt, 'delegated')
def evaluate_list(ast, context):
  print '<', evaluate(ast, context), '>'
send(context, 'addMethod', 'list', evaluate_list)
for ast_ in ast:
  send(ast_, 'eval', context)


####if __name__ == '__main__':
