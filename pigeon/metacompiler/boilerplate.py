

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
