from co import bootstrap, send
from la import setUpTransformEngine
from metaii import comp


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)


cola_metaii = r'''

  .SYNTAX PROGRAM

  literal = ( .STRING | .NUMBER ) .OUT('('*')') ;

  symbol = .ID .OUT(*) ;

  args = $ ( term .OUT(', ') ) ;

  list = '(' .OUT('(')
           what .OUT(', ') ( args | .EMPTY )
            ')' .OUT(')') ;

  define = 'define' .OUT('define, ') .ID .OUT('"'*'"') ;

  what = define | 'send' .OUT('send_ ') ;

  term = list | literal | symbol ;

  PROGRAM = .OUT('(') args .OUT(')') '.' ;

  .END

'''
cola_machine = comp(cola_metaii, open('metaii.asm').read())


def evaluate(context, it):
  if isinstance(it, tuple):
    if len(it) > 0:
      if callable(it[0]):
        g = it[0]
        args = (evaluate(context, foo) for foo in it[1:])
        return g(context, *args)
      return tuple(evaluate(context, foo) for foo in it)
  return it


def send_(context, receiver, name, *args):
  return send(receiver, name, *args)


def define(context, name, value):
  print 'assigning', name, value
  context[name] = value

c = {
  'define': define,
  'send_': send_,
  'symbol_vt': symbol_vt,
  }

def compile_(context, source):
  body = comp(source, cola_machine)
  print body
  ast = eval(body, context)
  print ast
  o = evaluate(context, ast)
  print o
  return body, ast, o

b, ast, o = compile_(c, '''
  ( define LIT
    ( send ( send symbol_vt 'allocate' ) 'setName' 'literal' ))

  ( define SYMBOL
    ( send ( send symbol_vt 'allocate' ) 'setName' 'symbol' ))

  
  .

''')

print b, ast, o
del c['__builtins__']
##lit = evaluate(c, o)



##  WORD := [ [ symbol_vt allocate ] setName '' ]
##  SEQ := [ [ symbol_vt allocate ] setName 'sequence' ]
##
##  context := [ object_vt delegated ]
##  [ context addMethod 'literal' emit_lit ]
##  [ context addMethod 'word' emit_word ]
##  [ context addMethod 'sequence' eval_seq ] 




##
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
##object_code = compile_('''
##
##  LIT := [ [ symbol_vt allocate ] setName 'literal' ]
##  WORD := [ [ symbol_vt allocate ] setName 'word' ]
##  SEQ := [ [ symbol_vt allocate ] setName 'sequence' ]
##
##  context := [ object_vt delegated ]
##  [ context addMethod 'literal' emit_lit ]
##  [ context addMethod 'word' emit_word ]
##  [ context addMethod 'sequence' eval_seq ] 
##  .
##
##''')
##
##
##namespace = object_code()
##
##
##LIT = namespace['LIT']
##WORD = namespace['WORD']
##SEQ = namespace['SEQ']
##CONTEXT = namespace['context']
##CONTEXT.indent = 0
##
##
##if __name__ == '__main__':
##  from pprint import pprint
##
##  source = '''
##  seq_vt := [ ast_vt delegated ]
##  [ seq_vt addMethod 'append' seq_append ]
##
##  s := [[ seq_vt allocate ] init SEQ +* ]
##
##  [ s append
##    [[ ast_vt allocate ] init WORD 'age' ]
##    [[ ast_vt allocate ] init LIT 'Danny' ]
##    [[ ast_vt allocate ] init LIT 23 ]
##    [[[ seq_vt allocate ] init SEQ +* ] append
##      [[ ast_vt allocate ] init LIT 1 ]
##      [[ ast_vt allocate ] init LIT 2 ]
##      [[ ast_vt allocate ] init LIT 3 ]
##    ]
##  ]
##
##  [ s eval CONTEXT ]
##  .
##  '''
##
##  a = compile_(source)
##  ast = a()
##  pprint(ast)
