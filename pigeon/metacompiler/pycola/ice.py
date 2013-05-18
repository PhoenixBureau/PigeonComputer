from co import bootstrap, send
from la import setUpTransformEngine


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)

LIT = send(symbol_vt, 'allocate')
send(LIT, 'setName', 'literal')

WORD = send(symbol_vt, 'allocate')
send(WORD, 'setName', 'word')

SEQ = send(symbol_vt, 'allocate')
send(SEQ, 'setName', 'sequence')


CONTEXT = send(object_vt, 'delegated')
CONTEXT.indent = 0

def emit_lit(ast, context):
  if not hasattr(context, 'indent'): context.indent = 0
  print ' ' * context.indent, repr(ast.data)
send(CONTEXT, 'addMethod', 'literal', emit_lit)

def emit_word(ast, context):
  if not hasattr(context, 'indent'): context.indent = 0
  print ' ' * context.indent, '< %s >' % (ast.data,)
send(CONTEXT, 'addMethod', 'word', emit_word)

def eval_seq(ast, context):
  if not hasattr(context, 'indent'): context.indent = 0
  context.indent += 3
  print ' ' * context.indent, '/----\\'
  for item in ast.data:
      send(item, 'eval', context)
  print ' ' * context.indent, '\\____/'
  context.indent -= 3
send(CONTEXT, 'addMethod', 'sequence', eval_seq)


if __name__ == '__main__':
    from metaii import comp
    from pprint import pprint

    machine = open('metaii.asm').read()
    cola_metaii = open('cola.metaii').read()

    cola_machine = comp(cola_metaii, machine)
    source = '''
    ! LIT [ symbol_vt <- allocate ] [ LIT <- setName 'literal' ]
    ! WORD [ symbol_vt <- allocate ] [ WORD <- setName 'word' ]
    ! SEQ [ symbol_vt <- allocate ] [ SEQ <- setName 'sequence' ]

    ! context [ object_vt <- delegated ]
    [ context <- addMethod 'literal' emit_lit ]
    [ context <- addMethod 'word' emit_word ]
    [ context <- addMethod 'sequence' eval_seq ] 

    ! ast [ ast_vt <- allocate ] [ ast <- init LIT 'Danny' ]
    [ ast <- eval context ]
    .
    '''

    body = 'def a():\n' + comp(source, cola_machine)
    print body
    exec body
    ast = a()
    pprint(ast)
##    a = ast[0]
##    print; print 'Evaluating', a
##    send(a, 'eval', CONTEXT)


##
##source = '''
##    2 4 add }
##    baz 'bar' foo q }
##    second ^ first }
##    ^^k } .
##    '''
