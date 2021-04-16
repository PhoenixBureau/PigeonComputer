    ADR PROGRAM
PROGRAM
    TST '▶'
    BF L1
    ID
    BE
    LB
    CL 'class '
    CI
    CL '_compiler:'
    NL
    LMI
    NL
    CL 'def compile(self, source):'
    LMI
    NL
    CL 'self.inbuf = source'
    NL
    CL 'self.pos = 0'
    NL
    CL 'self.outbuf = ""'
    NL
    CL 'self.margin = 0'
    NL
    CL 'self.gnlabel = 1'
    NL
    CL 'self.rule_'
    CI
    CL '()'
    NL
    CL 'return self.outbuf'
    LMD
    NL
    NL
L2
    CLL ST
    BT L2
    SET
    BE
    TST '◀'
    BE
L1
L3
    R
ST
    ID
    BF L4
    CL 'def rule_'
    CI
    CL '(self):'
    LMI
    NL
    CL 'rname = "'
    CI
    CL '"'
    NL
    CL 'rlabel = 0'
    NL
    TST '→'
    BE
    CLL EX1
    BE
    TST '▪'
    BE
    LMD
    NL
    NL
L4
L5
    R
EX1
    CLL EX2
    BF L6
L7
    TST '|'
    BF L8
    CL 'if not flag:'
    LMI
    NL
    CLL EX2
    BE
    LMD
    NL
L8
L9
    BT L7
    SET
    BE
L6
L10
    R
EX2
    CLL EX3
    BF L11
    CL 'if flag:'
    LMI
    NL
L11
    BT L12
    CLL OUTPUT
    BF L13
    CL 'if True:'
    LMI
    NL
L13
L12
    BF L14
L15
    CLL EX3
    BF L16
    CL 'if not flag: runBEjsfn(rname)'
    NL
    NL
L16
    BT L17
    CLL OUTPUT
    BF L18
L18
L17
    BT L15
    SET
    BE
    LMD
    NL
L14
L19
    R
EX3
    ID
    BF L20
    CL 'self.rule_'
    CI
    CL '()'
    NL
L20
    BT L21
    SR
    BF L22
    CL 'self.TST('
    CI
    CL ')'
    NL
L22
    BT L21
    TST '●'
    BF L23
    CL 'self.ID()'
    NL
L23
    BT L21
    TST 'ℕ'
    BF L24
    CL 'self.NUM()'
    NL
L24
    BT L21
    TST '≋'
    BF L25
    CL 'self.SR()'
    NL
L25
    BT L21
    TST '('
    BF L26
    CLL EX1
    BE
    TST ')'
    BE
L26
    BT L21
    TST '∅'
    BF L27
    CL 'self.SET()'
    NL
L27
    BT L21
    TST '★'
    BF L28
    CL 'self.SET()'
    NL
    CL 'while flag:'
    LMI
    NL
    CLL EX3
    BE
    LMD
    NL
    CL 'self.SET()'
    NL
L28
L21
    R
OUT1
    TST '⊙'
    BF L29
    TB
    CL 'CI'
    NL
L29
    BT L30
    SR
    BF L31
    TB
    CL 'CL '
    CI
    NL
L31
    BT L30
    TST '#'
    BF L32
    TB
    CL 'GN'
    NL
L32
    BT L30
    TST '↵'
    BF L33
    TB
    CL 'NL'
    NL
L33
    BT L30
    TST '⇤'
    BF L34
    TB
    CL 'LB'
    NL
L34
    BT L30
    TST '⇥'
    BF L35
    TB
    CL 'TB'
    NL
L35
    BT L30
    TST '↦'
    BF L36
    TB
    CL 'LMI'
    NL
L36
    BT L30
    TST '↤'
    BF L37
    TB
    CL 'LMD'
    NL
L37
L30
    R
OUTPUT
    TST '«'
    BF L38
L39
    CLL OUT1
    BT L39
    SET
    BE
    TST '»'
    BE
L38
L40
    R
    END

