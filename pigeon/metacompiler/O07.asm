	ADR PROGRAM
digit
	TST '0'
	BF L1
L1
	BT L2
	TST '1'
	BF L3
L3
	BT L2
	TST '2'
	BF L4
L4
	BT L2
	TST '3'
	BF L5
L5
	BT L2
	TST '4'
	BF L6
L6
	BT L2
	TST '5'
	BF L7
L7
	BT L2
	TST '6'
	BF L8
L8
	BT L2
	TST '7'
	BF L9
L9
	BT L2
	TST '8'
	BF L10
L10
	BT L2
	TST '9'
	BF L11
L11
L2
	R
hexDigit
	CLL digit
	BF L12
L12
	BT L13
	TST 'A'
	BF L14
L14
	BT L13
	TST 'B'
	BF L15
L15
	BT L13
	TST 'C'
	BF L16
L16
	BT L13
	TST 'D'
	BF L17
L17
	BT L13
	TST 'E'
	BF L18
L18
	BT L13
	TST 'F'
	BF L19
L19
L13
	R
ident
	ID
	BF L20
	CL 'ident '
	CI
	OUT
L20
L21
	R
qualident
	CLL ident
	BF L22
	TST '.'
	BE
L22
L23
	BF L24
L24
	BT L25
	SET
	BF L26
L26
L25
	BF L27
	CLL ident
	BE
	CL 'qualident'
	OUT
L27
L28
	R
identdef
	CLL ident
	BF L29
	TST '*'
	BF L30
	CL ' export'
	OUT
L30
	BT L31
	SET
	BF L32
L32
L31
	BE
L29
L33
	R
integer
	CLL digit
	BF L34
L35
	CLL digit
	BT L35
	SET
	BE
L34
L36
	BF L37
L37
	BT L38
	CLL digit
	BF L39
L40
	CLL hexDigit
	BT L40
	SET
	BE
	TST 'H'
	BE
L39
L41
	BF L42
L42
L38
	R
real
	CLL digit
	BF L43
L44
	CLL digit
	BT L44
	SET
	BE
	TST '.'
	BE
L45
	CLL digit
	BT L45
	SET
	BE
	CLL ScaleFactor
	BF L46
L46
	BT L47
	SET
	BF L48
L48
L47
	BE
L43
L49
	R
ScaleFactor
	TST 'E'
	BF L50
L50
	BT L51
	TST 'D'
	BF L52
L52
L51
	BF L53
	TST '+'
	BF L54
L54
	BT L55
	TST '-'
	BF L56
L56
L55
	BF L57
L57
	BT L58
	SET
	BF L59
L59
L58
	BE
	CLL digit
	BE
L60
	CLL digit
	BT L60
	SET
	BE
L53
L61
	R
number
	CLL integer
	BF L62
L62
	BT L63
	CLL real
	BF L64
L64
L63
	BF L65
	CL 'number'
	OUT
L65
L66
	R
string
	TST '"'
	BF L67
	SR
	BE
	TST '"'
	BE
L67
L68
	BF L69
L69
	BT L70
	CLL digit
	BF L71
L72
	CLL hexDigit
	BT L72
	SET
	BE
	TST 'H'
	BE
L71
L73
	BF L74
L74
L70
	R
ConstantDeclaration
	CLL identdef
	BF L75
	TST '='
	BE
	CLL ConstExpression
	BE
L75
L76
	R
ConstExpression
	CLL expression
	BF L77
L77
L78
	R
TypeDeclaration
	CLL identdef
	BF L79
	CL 'TypeDeclaration'
	OUT
	TST '='
	BE
	CLL StrucType
	BE
	CL 'TypeDeclaration_Type'
	OUT
L79
L80
	R
StrucType
	CLL ArrayType
	BF L81
L81
	BT L82
	CLL RecordType
	BF L83
L83
	BT L82
	CLL PointerType
	BF L84
L84
	BT L82
	CLL ProcedureType
	BF L85
L85
L82
	R
type
	CLL qualident
	BF L86
L86
	BT L87
	CLL StrucType
	BF L88
L88
L87
	R
ArrayType
	TST 'ARRAY'
	BF L89
	CLL length
	BE
L90
	TST ','
	BF L91
	CLL length
	BE
L91
L92
	BT L90
	SET
	BE
	TST 'OF'
	BE
	CLL type
	BE
L89
L93
	R
length
	NUM
	BF L94
L94
L95
	R
RecordType
	TST 'RECORD'
	BF L96
	TST '('
	BF L97
	CLL BaseType
	BE
	TST ')'
	BE
L97
L98
	BF L99
L99
	BT L100
	SET
	BF L101
L101
L100
	BE
	CLL FieldListSequence
	BF L102
L102
	BT L103
	SET
	BF L104
L104
L103
	BE
	TST 'END'
	BE
L96
L105
	R
BaseType
	CLL qualident
	BF L106
L106
L107
	R
FieldListSequence
	CLL FieldList
	BF L108
L109
	TST ';'
	BF L110
	CLL FieldList
	BE
L110
L111
	BT L109
	SET
	BE
L108
L112
	R
FieldList
	CLL IdentList
	BF L113
	TST ':'
	BE
	CLL type
	BE
L113
L114
	R
IdentList
	CLL identdef
	BF L115
L116
	TST ','
	BF L117
	CLL identdef
	BE
L117
L118
	BT L116
	SET
	BE
L115
L119
	R
PointerType
	TST 'POINTER'
	BF L120
	TST 'TO'
	BE
	CLL type
	BE
L120
L121
	R
ProcedureType
	TST 'PROCEDURE'
	BF L122
	TST 'FormalParameters'
	BF L123
L123
	BT L124
	SET
	BF L125
L125
L124
	BE
L122
L126
	R
VariableDeclaration
	CLL IdentList
	BF L127
	TST ':'
	BE
	CLL type
	BE
L127
L128
	R
expression
	CLL SimpleExpression
	BF L129
L130
	CLL relation
	BF L131
	CLL SimpleExpression
	BE
L131
L132
	BT L130
	SET
	BE
L129
L133
	R
relation
	TST '='
	BF L134
L134
	BT L135
	TST '#'
	BF L136
L136
	BT L135
	TST '<'
	BF L137
L137
	BT L135
	TST '<='
	BF L138
L138
	BT L135
	TST '>'
	BF L139
L139
	BT L135
	TST '>='
	BF L140
L140
	BT L135
	TST 'IN'
	BF L141
L141
	BT L135
	TST 'IS'
	BF L142
L142
L135
	R
SimpleExpression
	TST '+'
	BF L143
L143
	BT L144
	TST '-'
	BF L145
L145
L144
	BF L146
L146
	BT L147
	SET
	BF L148
L148
L147
	BF L149
	CLL term
	BE
L150
	CLL AddOperator
	BF L151
	CLL term
	BE
L151
L152
	BT L150
	SET
	BE
L149
L153
	R
AddOperator
	TST '+'
	BF L154
L154
	BT L155
	TST '-'
	BF L156
L156
	BT L155
	TST 'OR'
	BF L157
L157
L155
	R
term
	CLL factor
	BF L158
L159
	CLL MulOperator
	BF L160
	CLL factor
	BE
L160
L161
	BT L159
	SET
	BE
L158
L162
	R
MulOperator
	TST '*'
	BF L163
L163
	BT L164
	TST '/'
	BF L165
L165
	BT L164
	TST 'DIV'
	BF L166
L166
	BT L164
	TST 'MOD'
	BF L167
L167
	BT L164
	TST '&'
	BF L168
L168
L164
	R
factor
	CLL number
	BF L169
L169
	BT L170
	CLL string
	BF L171
L171
	BT L170
	TST 'NIL'
	BF L172
L172
	BT L170
	TST 'TRUE'
	BF L173
L173
	BT L170
	TST 'FALSE'
	BF L174
L174
	BT L170
	TST '('
	BF L175
	CLL expression
	BE
	TST ')'
	BE
L175
	BT L170
	TST '~'
	BF L176
	CLL factor
	BE
L176
L170
	R
CD
	CLL ConstantDeclaration
	BF L177
	TST ';'
	BE
L177
L178
	BF L179
L179
	BT L180
	SET
	BF L181
L181
L180
	R
DeclarationSequence
	TST 'CONST'
	BF L182
	CL 'const'
	OUT
	CLL CD
	BE
L182
L183
	BF L184
	TST 'TYPE'
	BF L185
	CL 'types'
	OUT
	CLL TypeDeclaration
	BE
	TST ';'
	BE
L185
L186
	BE
L184
L187
	R
PROGRAM
	TST 'MODULE'
	BF L188
	CLL ident
	BE
	TST ';'
	BE
	CL 'module'
	OUT
	CLL DeclarationSequence
	BE
	TST 'END'
	BE
	CLL ident
	BE
	TST '.'
	BE
	CL 'end_module'
	OUT
L188
L189
	R
	END

