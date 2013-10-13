from co import bootstrap, send
from la import setUpTransformEngine
from metaii import comp


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)


cola_metaii = r'''

  .SYNTAX PROGRAM

  args = $ ( term .OUT(', ') ) ;

  sending = '[' .OUT('( send,') term .OUT(', ')
                .ID .OUT('"'*'",')
                ( args | .EMPTY )
            ']' .OUT(')') ;

  literal = ( .STRING | .NUMBER ) .OUT('('*')') ;

  symbol = .ID .OUT(*) ;

  new_list = '+*' .OUT('[]') ;

  term = sending | literal | symbol | new_list ;

  store = .ID .OUT(*' = \') ':=' term ;

  it = store | sending ;

  PROGRAM = it $ it '.' .OUT('return locals()') ;

  .END

'''
cola_machine = comp(cola_metaii, open('metaii.asm').read())


def evaluate(it):
  if isinstance(it, tuple) and len(it) > 0 and callable(it[0]):
    return it[0](*map(evaluate, it[1:]))
  return it


def compile_(source, compiler=cola_machine):
  body = 'def a():\n' + comp(source, cola_machine)
  if __debug__:
    print body
  exec body
  return a


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

def seq_append(seq, *things):
  seq.data.extend(things)
  return seq


object_code = compile_('''

  sym := [ symbol_vt allocate ]

  LIT := [ sym setName 'literal' ]
  WORD := [ sym setName 'word' ]
  SEQ := [ sym setName 'sequence' ]

  context := [ object_vt delegated ]
  [ context addMethod 'literal' emit_lit ]
  [ context addMethod 'word' emit_word ]
  [ context addMethod 'sequence' eval_seq ] 
  .

''')


namespace = object_code()


LIT = evaluate(namespace['LIT'])
WORD = evaluate(namespace['WORD'])
SEQ = evaluate(namespace['SEQ'])
CONTEXT = evaluate(namespace['context'])
CONTEXT.indent = 0


if __name__ == '__main__':
  from pprint import pprint

  source = '''
  seq_vt := [ ast_vt delegated ]
  [ seq_vt addMethod 'append' seq_append ]

  s := [[ seq_vt allocate ] init SEQ +* ]

  [ s append
    [[ ast_vt allocate ] init WORD 'age' ]
    [[ ast_vt allocate ] init LIT 'Danny' ]
    [[ ast_vt allocate ] init LIT 23 ]
    [[[ seq_vt allocate ] init SEQ +* ] append
      [[ ast_vt allocate ] init LIT 1 ]
      [[ ast_vt allocate ] init LIT 2 ]
      [[ ast_vt allocate ] init LIT 3 ]
    ]
  ]

  [ s eval CONTEXT ]
  .
  '''

  a = compile_(source)
  ast = a()
  pprint(ast)
