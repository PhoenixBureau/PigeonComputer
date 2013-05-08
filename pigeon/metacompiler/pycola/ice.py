from co import bootstrap, send
from la import setUpTransformEngine


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)

LIT = send(symbol_vt, 'allocate')
send(LIT, 'setName', 'literal')

EVAL = send(symbol_vt, 'allocate')
send(EVAL, 'setName', 'eval')

ast = send(ast_vt, 'allocate')
send(ast, 'init', LIT, 23)

e = send(ast_vt, 'allocate')
send(e, 'init', EVAL, ast)


context_vt = send(vtvt, 'delegated')

def emit(thing, context):
    print thing.data
send(context_vt, 'addMethod', 'literal', emit)

send(context_vt, 'addMethod', 'eval',
     lambda thing, context: send(ast, 'eval', context))


print ast.symbol.name, ast.data
print e.symbol.name, e.data

send(ast, 'eval', context_vt)
send(e, 'eval', context_vt)




def a():
	frame = []
	stack = [frame]
	ast = send(ast_vt, "allocate");send(ast, "init", LIT, 23);frame.append(ast)
	ast = send(ast_vt, "allocate");send(ast, "init", LIT, 18);frame.append(ast)
	frame.append("add");frame=[];stack.append(frame)
	ast = send(ast_vt, "allocate");send(ast, "init", LIT, 'b');frame.append(ast)
	ast = send(ast_vt, "allocate");send(ast, "init", LIT, 23);frame.append(ast)
	frame.append("Hi");frame=[];stack.append(frame)
	frame.append("c");frame=[];stack.append(frame)
	return stack
