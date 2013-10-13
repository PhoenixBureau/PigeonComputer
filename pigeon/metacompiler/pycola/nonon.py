from pprint import pprint
from co import bootstrap, send
from la import setUpTransformEngine
from metaii import comp


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)


def allocate(vt): return send(vt, 'allocate')
def make_kind(kind): return send(allocate(symbol_vt), 'setName', kind)
def make_ast(KIND, value): return send(allocate(ast_vt), 'init', KIND, value)


SYMBOL = make_kind('symbol')
LITERAL = make_kind('literal')
LIST = make_kind('list')


def symbol(name): return make_ast(SYMBOL, name)
def literal(value): return make_ast(LITERAL, value)
def list_(*values): return make_ast(LIST, list(values))


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


def evaluate(ast, context):
  symbol = send(ast, 'typeOf')
  sname = send(symbol, 'getName')

  if sname == 'symbol':
    try:
      return send(context, 'lookup', ast.data)
    except:
      return ast.data

  if sname == 'literal':
    return ast.data

  first, rest = ast.data[0], ast.data[1:]
  symbol = send(first, 'typeOf')
  sname = send(symbol, 'getName')

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

def evaluate_list(ast, context):
  print '<', evaluate(ast, context), '>'


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
cola_machine = comp(cola_metaii, open('metaii.asm').read())

source = '''
(define a 1)
(a)

 (define area (lambda (r) (m 3.141592653 (multiply r r))))
 ( area cage nic )
 ( 12 'neato' )
.
'''

body = comp(source, cola_machine)
print body
print

ast = eval(body)

pprint(ast)
print

context = send(object_vt, 'delegated')
send(context, 'addMethod', 'list', evaluate_list)
for ast_ in ast:
  send(ast_, 'eval', context)


####if __name__ == '__main__':
