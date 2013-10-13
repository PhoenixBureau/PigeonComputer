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
LAMBDA = send(send(symbol_vt, 'allocate'), 'setName', 'lambda')

def symbol(name):
  try:
    return send(context, 'lookup', name)
  except:
    symbol = send(ast_vt, 'allocate')
    send(symbol, 'init', SYMBOL, name)
    send(context, 'addMethod', name, symbol)
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
    for k, v in zip(variables, args.data):
      send(new_context, 'addMethod', k, v)
    send(exp, 'eval', new_context)

  inner_ast = send(ast_vt, 'allocate')
  send(inner_ast, 'init', LAMBDA, inner)
  return inner_ast

def emit_lit(ast, context):
  print repr(ast.data)

def emit_symbol(ast, context):
  print '< %s >' % (ast.data,)

def eval_list(ast, context):
  if len(ast.data) > 0:
    f, rest = ast.data[0], ast.data[1:]
    symbol = send(f, 'typeOf')
    sname = send(symbol, 'getName')
    if sname == 'symbol':

      if f.data == 'define':
        var, exp = rest
        var = var.data
        value = eval_list(exp, context)
        send(context, 'addMethod', var, value)

      elif f.data == 'lambda':
        variables, exp = rest
        return make_lambda_ast(variables, exp, context)

      i = send(context, 'lookup', f.data).data
      i(rest)
      return

  for item in ast.data:
      send(item, 'eval', context)

send(context, 'addMethod', 'list', eval_list)
send(context, 'addMethod', 'symbol', emit_symbol)
send(context, 'addMethod', 'literal', emit_lit)


cola_metaii = r'''

  .SYNTAX PROGRAM

  literal = ( .STRING | .NUMBER ) .OUT('literal('*')') ;

  symbol = .ID .OUT('symbol("'*'")') ;

  args = $ ( term .OUT(', ') ) ;

  list = '(' .OUT('list_(')
           term .OUT(', ') ( args | .EMPTY )
            ')' .OUT(')') ;

  define = 'define' .OUT('define, ') .ID .OUT('"'*'"') ;

  enifed = 'enifed' .OUT('enifed, ') .ID .OUT('"'*'"') ;

  what = define | enifed | 'send' .OUT('send_ ') ;

  term = list | literal | symbol ;

  PROGRAM = .OUT('(') args .OUT(')') '.' ;

  .END

'''
cola_machine = comp(cola_metaii, open('metaii.asm').read())

source = '''
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


##def evaluate(ast, context):
##  
##  if isinstance(it, tuple):
##    if len(it) > 0:
##      if callable(it[0]):
##        g = it[0]
##        args = (evaluate(context, foo) for foo in it[1:])
##        return g(context, *args)
##      return tuple(evaluate(context, foo) for foo in it)
##  return it



##send(c, 'addMethod', 'literal',  (lambda ast, context: repr(ast.data))
##send(c, 'addMethod', 'garry', 23)
##send(c, 'lookup', 'garry')


##def send_(context, receiver, name, *args):
##  return send(receiver, name, *args)
##
##
##def define(context, name, value):
##  print 'assigning', name, value
##  context[name] = value
##
##def enifed(context, name):
##  return context[name]
##
##
##
##def emit_lit(ast, context):
##  print ' ' * context.indent, repr(ast.data)
##
##def emit_word(ast, context):
##  print ' ' * context.indent, '< %s >' % (ast.data,)
##
##def eval_seq(ast, context):
##  context.indent += 3
##  print ' ' * context.indent, '/----\\'
##  for item in ast.data:
##      send(item, 'eval', context)
##  print ' ' * context.indent, '\\____/'
##  context.indent -= 3
##
##def seq_append(seq, *things):
##  seq.data.extend(things)
##  return seq
##
##
##c = {
##  'define': define,
##  'enifed': enifed,
##  'send_': send_,
##  'symbol_vt': symbol_vt,
##  'object_vt': object_vt,
##  'ast_vt': ast_vt,
##  'emit_lit': emit_lit,
##  'emit_word': emit_word,
##  'eval_seq': eval_seq,
##  }
##
##def compile_(context, source):
##  body = comp(source, cola_machine)
##  print body
##  ast = eval(body, context)
##  print ast
##  o = evaluate(context, ast)
##  print o
##  return body, ast, o
##
##b, ast, o = compile_(c, '''
##  ( define LIT
##    ( send ( send symbol_vt 'allocate' ) 'setName' 'literal' ))
##
##  ( define WORD
##    ( send ( send symbol_vt 'allocate' ) 'setName' 'word' ))
##
##  ( define SEQ
##    ( send ( send symbol_vt 'allocate' ) 'setName' 'sequence' ))
##
##  ( define context ( send object_vt 'delegated' ) )
##
##  ( send ( enifed context ) 'addMethod' 'literal' emit_lit )
##  ( send ( enifed context ) 'addMethod' 'word' emit_word )
##  ( send ( enifed context ) 'addMethod' 'sequence' eval_seq )
##
##  ( define s 
##    ( send ( send ast_vt 'allocate') 'init' ( enifed WORD ) 'age' )
##    )
##  .
##
##''')
##
##
##
##print b, ast, o
##del c['__builtins__']
##c['context'].indent = 0
##
##
####if __name__ == '__main__':
####  from pprint import pprint
####
####  source = '''
####  seq_vt := [ ast_vt delegated ]
####  [ seq_vt addMethod 'append' seq_append ]
####
####  s := [[ seq_vt allocate ] init SEQ +* ]
####
####  [ s append
####    [[ ast_vt allocate ] init WORD 'age' ]
####    [[ ast_vt allocate ] init LIT 'Danny' ]
####    [[ ast_vt allocate ] init LIT 23 ]
####    [[[ seq_vt allocate ] init SEQ +* ] append
####      [[ ast_vt allocate ] init LIT 1 ]
####      [[ ast_vt allocate ] init LIT 2 ]
####      [[ ast_vt allocate ] init LIT 3 ]
####    ]
####  ]
####
####  [ s eval CONTEXT ]
####  .
####  '''
####
####  a = compile_(source)
####  ast = a()
####  pprint(ast)
