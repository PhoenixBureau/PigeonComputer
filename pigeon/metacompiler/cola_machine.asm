	ADR PROGRAM
string
	SR
	BF L1
	CL 'ast = send(ast_vt, "allocate")'
	OUT
	CL 'send(ast, "init", LIT, '
	CI
	CL ')'
	OUT
	CL 'frame.append(ast)'
	OUT
L1
L2
	R
number
	NUM
	BF L3
	CL 'ast = send(ast_vt, "allocate")'
	OUT
	CL 'send(ast, "init", LIT, '
	CI
	CL ')'
	OUT
	CL 'frame.append(ast)'
	OUT
L3
L4
	R
symbol
	ID
	BF L5
	CL 'frame.append("'
	CI
	CL '")'
	OUT
L5
L6
	R
pound
	TST '#'
	BF L7
	CL 'frame=[]'
	OUT
	CL 'stack.append(frame)'
	OUT
L7
L8
	R
bang
	TST '!'
	BF L9
	CL 'frame.append(stack.pop(-2))'
	OUT
L9
L10
	R
term
	CLL string
	BF L11
L11
	BT L12
	CLL number
	BF L13
L13
	BT L12
	CLL symbol
	BF L14
L14
	BT L12
	CLL pound
	BF L15
L15
	BT L12
	CLL bang
	BF L16
L16
L12
	R
PROGRAM
	CL 'frame = []'
	OUT
	CL 'stack = [frame]'
	OUT
	CLL term
	BE
L17
	CLL term
	BT L17
	SET
	BE
	TST '.'
	BE
	CL 'return stack'
	OUT
L18
L19
	R
	END

