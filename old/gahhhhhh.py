from co import bootstrap, send
from la import setUpTransformEngine


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)


def p(*a):
  print a


context_vt = send(vtvt, 'delegated')
send(context_vt, 'addMethod', 'bil', lambda *args: p(args[0] is c))

c = send(context_vt, 'allocate')
send(c, 'bil')
##send(i, 'bil')



'''

     [context addMethod [[context allocate] makekind 'symbol']  'SYMBOL']
     [[context allocate] makeast [context lookup 'SYMBOL'] 'Barry']

     [ context addMethod 'twentythree' 23 ]
     ( twentythree )
     ( ooo [ context addMethod 'g' [context lookup 'twentythree'] ])

     (define p (divide 1 1000000000))
     (define pi (multiply 3141592653 p))
     (pi p)
     (define area (lambda (r) (multiply pi (multiply r r))))
     ( area 23 nic )

     ( 12 'neato' )


'''
