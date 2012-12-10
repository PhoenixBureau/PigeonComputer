	ADR PROGRAM
OUT1
	TST '*1'
	BF L1
	CL 'gen_label_1()'
	OUT
L1
	BT L2
	TST '*2'
	BF L3
	CL 'gen_label_2()'
	OUT
L3
	BT L2
	TST '*'
	BF L4
	CL 'copy_input()'
	OUT
L4
	BT L2
	SR
	BF L5
	CL 'copy_literal('
	CI
	CL ')'
	OUT
L5
L2
	R
OUTPUT
	TST '.OUT'
	BF L6
	TST '('
	BE
L7
	CLL OUT1
	BT L7
	SET
	BE
	TST ')'
	BE
L6
	BT L8
	TST '.LABEL'
	BF L9
	CL 'LB'
	OUT
	CLL OUT1
	BE
L9
L8
	BF L10
	CL 'output_line()'
	OUT
L10
L11
	R
EX3
	ID
	BF L12
	CL 'call('
	CI
	CL ')'
	OUT
L12
	BT L13
	SR
	BF L14
	CL 'startswith('
	CI
	CL ')'
	OUT
L14
	BT L13
	TST '.ID'
	BF L15
	CL 'identifier()'
	OUT
L15
	BT L13
	TST '.NUMBER'
	BF L16
	CL 'number()'
	OUT
L16
	BT L13
	TST '.STRING'
	BF L17
	CL 'string()'
	OUT
L17
	BT L13
	TST '('
	BF L18
	CLL EX1
	BE
	TST ')'
	BE
L18
	BT L13
	TST '.EMPTY'
	BF L19
	CL 'sbr(switch_reg, 1 << switch_bit)'
	OUT
L19
	BT L13
	TST '$'
	BF L20
	CL 'label('
	GN1
	CL ')'
	OUT
	CLL EX3
	BE
	CL 'sbrc(switch_reg, switch_bit)'
	OUT
	CL 'jmp('
	GN1
	CL ')'
	OUT
	CL 'sbr(switch_reg, 1 << switch_bit)'
	OUT
L20
L13
	R
EX2
	CLL EX3
	BF L21
	CL 'sbrs(switch_reg, switch_bit)'
	OUT
	CL 'jmp('
	GN1
	CL ')'
	OUT
L21
	BT L22
	CLL OUTPUT
	BF L23
L23
L22
	BF L24
L25
	CLL EX3
	BF L26
	CL 'sbrs(switch_reg, switch_bit)'
	OUT
	CL 'jmp(ERROR)'
	OUT
L26
	BT L27
	CLL OUTPUT
	BF L28
L28
L27
	BT L25
	SET
	BE
	CL 'label('
	GN1
	CL ')'
	OUT
L24
L29
	R
EX1
	CLL EX2
	BF L30
L31
	TST '|'
	BF L32
	CL 'sbrc(switch_reg, switch_bit)'
	OUT
	CL 'jmp('
	GN1
	CL ')'
	OUT
	CLL EX2
	BE
L32
L33
	BT L31
	SET
	BE
	CL 'label('
	GN1
	CL ')'
	OUT
L30
L34
	R
ST
	ID
	BF L35
	CL 'label('
	CI
	CL ') # subroutine =========='
	OUT
	TST '='
	BE
	CLL EX1
	BE
	TST ';'
	BE
	CL 'ret()'
	OUT
	CL ''
	OUT
L35
L36
	R
PROGRAM
	TST '.SYNTAX'
	BF L37
	ID
	BE
	CL 'define(switch_bit=0)'
	OUT
	CL 'define(switch_reg=r0)'
	OUT
	CL ''
	OUT
	CL 'label('
	CI
	CL ')'
	OUT
L38
	CLL ST
	BT L38
	SET
	BE
	TST '.END'
	BE
	CL '#END'
	OUT
L37
L39
	R
	END

