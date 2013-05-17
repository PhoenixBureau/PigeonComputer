from co import bootstrap, send
from la import setUpTransformEngine


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)

LIT = send(symbol_vt, 'allocate')
send(LIT, 'setName', 'literal')


if __name__ == '__main__':
    from metaii import comp
    from pprint import pprint


    machine = open('metaii.asm').read()
    cola_metaii = open('cola.metaii').read()

    cola_machine = comp(cola_metaii, machine)
    source = '''
    two four add #
    baz bar foo seq #
    second first ! #
    !!k .
    '''

    [('k',
  ('add', 'four', 'two'),
  (('seq', 'foo', 'bar', 'baz'), 'first', 'second'))]

##    'b' 23 Hi ! #
##    add
##    Say goodnight Gracie #
##    Goodnight Gracie ! .
##    '''
##    
##    Goodnight Gracie !
##    ! ! c
##    .
##    '''

    body = 'def a():\n' + comp(source, cola_machine)
    exec body
    pprint(a())
