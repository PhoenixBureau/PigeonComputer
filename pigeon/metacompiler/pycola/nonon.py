from pprint import pprint
from co import bootstrap, send
from la import setUpTransformEngine
from metaii import comp


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)


c = context = send(object_vt, 'delegated')


SYMBOL = send(send(symbol_vt, 'allocate'), 'setName', 'symbol')
LITERAL = send(send(symbol_vt, 'allocate'), 'setName', 'literal')
LIST = send(send(symbol_vt, 'allocate'), 'setName', 'list')


def symbol(name):
  symbol = send(ast_vt, 'allocate')
  send(symbol, 'init', SYMBOL, name)
  return symbol

def literal(value):
  lit = send(ast_vt, 'allocate')
  send(lit, 'init', LITERAL, value)
  return lit

def list_(*values):
  el = send(ast_vt, 'allocate')
  send(el, 'init', LIST, list(values))
  return el



def make_lambda_ast(variables, exp, context):
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
      variables, exp = rest
      return make_lambda_ast(variables, exp, context)

  exp = tuple(evaluate(it, context) for it in ast.data)
  if callable(exp[0]):
    return exp[0](*exp[1:])

  return exp

def evaluate_list(ast, context):
  print '<', evaluate(ast, context), '>'

send(context, 'addMethod', 'list', evaluate_list)


cola_metaii = r'''

  .SYNTAX PROGRAM

  literal = ( .STRING | .NUMBER ) .OUT('literal('*')') ;

  symbol = .ID .OUT('symbol("'*'")') ;

  args = $ term ;

  list = '(' .OUT('list_(')
           term ( args | .EMPTY )
            ')' .OUT(')') ;

  term = ( list | literal | symbol ) .OUT(', ') ;

  PROGRAM = .OUT('(') args .OUT(')') '.' ;

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

for ast_ in ast:
  send(ast_, 'eval', context)


####if __name__ == '__main__':
