class PROGRAMCompiler:

    def compile(self, source):
        self.inbuf = source
        self.pos = 0
        self.outbuf = ""
        self.margin = 0
        self.gnlabel = 1
        self.rule_PROGRAM()
        return self.outbuf

PROGRAM
        TST '▶'
        BF L1
        ID
        BE
        LB
        CL 'class '
        CI
        CL 'Compiler:'
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
OUT1
        TST '⊙'
        BF L4
        TB
        CL 'CI'
        NL
L4
        BT L5
        SR
        BF L6
        TB
        CL 'CL '
        CI
        NL
L6
        BT L5
        TST '#'
        BF L7
        TB
        CL 'GN'
        NL
L7
        BT L5
        TST '↵'
        BF L8
        TB
        CL 'NL'
        NL
L8
        BT L5
        TST '⇤'
        BF L9
        TB
        CL 'LB'
        NL
L9
        BT L5
        TST '⇥'
        BF L10
        TB
        CL 'TB'
        NL
L10
        BT L5
        TST '↦'
        BF L11
        TB
        CL 'LMI'
        NL
L11
        BT L5
        TST '↤'
        BF L12
        TB
        CL 'LMD'
        NL
L12
L5
        R
OUTPUT
        TST '«'
        BF L13
L14
        CLL OUT1
        BT L14
        SET
        BE
        TST '»'
        BE
L13
L15
        R
EX3
        ID
        BF L16
        TB
        CL 'CLL '
        CI
        NL
L16
        BT L17
        SR
        BF L18
        TB
        CL 'TST '
        CI
        NL
L18
        BT L17
        TST '●'
        BF L19
        TB
        CL 'ID'
        NL
L19
        BT L17
        TST 'ℕ'
        BF L20
        TB
        CL 'NUM'
        NL
L20
        BT L17
        TST '≋'
        BF L21
        TB
        CL 'SR'
        NL
L21
        BT L17
        TST '('
        BF L22
        CLL EX1
        BE
        TST ')'
        BE
L22
        BT L17
        TST '∅'
        BF L23
        TB
        CL 'SET'
        NL
L23
        BT L17
        TST '★'
        BF L24
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
L24
L17
        R
EX2
        CLL EX3
        BF L25
        TB
        CL 'BF L'
        GN
        NL
L25
        BT L26
        CLL OUTPUT
        BF L27
L27
L26
        BF L28
L29
        CLL EX3
        BF L30
        TB
        CL 'BE'
        NL
L30
        BT L31
        CLL OUTPUT
        BF L32
L32
L31
        BT L29
        SET
        BE
        LB
        CL 'L'
        GN
        NL
L28
L33
        R
EX1
        CLL EX2
        BF L34
L35
        TST '|'
        BF L36
        TB
        CL 'BT L'
        GN
        NL
        CLL EX2
        BE
L36
L37
        BT L35
        SET
        BE
        LB
        CL 'L'
        GN
        NL
L34
L38
        R
ST
        ID
        BF L39
        LB
        CI
        NL
        TST '→'
        BE
        CLL EX1
        BE
        TST '▪'
        BE
        TB
        CL 'R'
        NL
L39
L40
        R

