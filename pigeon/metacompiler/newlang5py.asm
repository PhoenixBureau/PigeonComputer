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
OUT1
    TST '⊙'
    BF L11
    TB
    CL 'CI'
    NL
L11
    BT L12
    SR
    BF L13
    TB
    CL 'CL '
    CI
    NL
L13
    BT L12
    TST '#'
    BF L14
    TB
    CL 'GN'
    NL
L14
    BT L12
    TST '↵'
    BF L15
    TB
    CL 'NL'
    NL
L15
    BT L12
    TST '⇤'
    BF L16
    TB
    CL 'LB'
    NL
L16
    BT L12
    TST '⇥'
    BF L17
    TB
    CL 'TB'
    NL
L17
    BT L12
    TST '↦'
    BF L18
    TB
    CL 'LMI'
    NL
L18
    BT L12
    TST '↤'
    BF L19
    TB
    CL 'LMD'
    NL
L19
L12
    R
OUTPUT
    TST '«'
    BF L20
L21
    CLL OUT1
    BT L21
    SET
    BE
    TST '»'
    BE
L20
L22
    R
EX3
    ID
    BF L23
    TB
    CL 'CLL '
    CI
    NL
L23
    BT L24
    SR
    BF L25
    TB
    CL 'TST '
    CI
    NL
L25
    BT L24
    TST '●'
    BF L26
    TB
    CL 'ID'
    NL
L26
    BT L24
    TST 'ℕ'
    BF L27
    TB
    CL 'NUM'
    NL
L27
    BT L24
    TST '≋'
    BF L28
    TB
    CL 'SR'
    NL
L28
    BT L24
    TST '('
    BF L29
    CLL EX1
    BE
    TST ')'
    BE
L29
    BT L24
    TST '∅'
    BF L30
    TB
    CL 'SET'
    NL
L30
    BT L24
    TST '★'
    BF L31
    LB
    CL 'L'
    GN
    NL
    CLL EX3
    BE
    TB
    CL 'BT L'
    GN
    NL
    TB
    CL 'SET'
    NL
L31
L24
    R
EX2
    CLL EX3
    BF L32
    TB
    CL 'BF L'
    GN
    NL
L32
    BT L33
    CLL OUTPUT
    BF L34
L34
L33
    BF L35
L36
    CLL EX3
    BF L37
    TB
    CL 'BE'
    NL
L37
    BT L38
    CLL OUTPUT
    BF L39
L39
L38
    BT L36
    SET
    BE
    LB
    CL 'L'
    GN
    NL
L35
L40
    R
    END

