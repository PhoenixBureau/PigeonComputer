class PROGRAM_compiler:

    def compile(self, source):
        self.inbuf = source
        self.pos = 0
        self.outbuf = ""
        self.margin = 0
        self.gnlabel = 1
        self.rule_PROGRAM()
        return self.outbuf

    def rule_PROGRAM(self):
        rname = "PROGRAM"
        rlabel = 0
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


    def rule_ST(self):
        rname = "ST"
        rlabel = 0
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


    def rule_OUT1(self):
        rname = "OUT1"
        rlabel = 0
            TST '⊙'
            BF L6
            TB
            CL 'CI'
            NL
L6
            BT L7
            SR
            BF L8
            TB
            CL 'CL '
            CI
            NL
L8
            BT L7
            TST '#'
            BF L9
            TB
            CL 'GN'
            NL
L9
            BT L7
            TST '↵'
            BF L10
            TB
            CL 'NL'
            NL
L10
            BT L7
            TST '⇤'
            BF L11
            TB
            CL 'LB'
            NL
L11
            BT L7
            TST '⇥'
            BF L12
            TB
            CL 'TB'
            NL
L12
            BT L7
            TST '↦'
            BF L13
            TB
            CL 'LMI'
            NL
L13
            BT L7
            TST '↤'
            BF L14
            TB
            CL 'LMD'
            NL
L14
L7


    def rule_OUTPUT(self):
        rname = "OUTPUT"
        rlabel = 0
            TST '«'
            BF L15
L16
            CLL OUT1
            BT L16
            SET
            BE
            TST '»'
            BE
L15
L17


    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
            ID
            BF L18
            TB
            CL 'CLL '
            CI
            NL
L18
            BT L19
            SR
            BF L20
            TB
            CL 'TST '
            CI
            NL
L20
            BT L19
            TST '●'
            BF L21
            TB
            CL 'ID'
            NL
L21
            BT L19
            TST 'ℕ'
            BF L22
            TB
            CL 'NUM'
            NL
L22
            BT L19
            TST '≋'
            BF L23
            TB
            CL 'SR'
            NL
L23
            BT L19
            TST '('
            BF L24
            CLL EX1
            BE
            TST ')'
            BE
L24
            BT L19
            TST '∅'
            BF L25
            TB
            CL 'SET'
            NL
L25
            BT L19
            TST '★'
            BF L26
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
L26
L19


    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
            CLL EX3
            BF L27
            TB
            CL 'BF L'
            GN
            NL
L27
            BT L28
            CLL OUTPUT
            BF L29
L29
L28
            BF L30
L31
            CLL EX3
            BF L32
            TB
            CL 'BE'
            NL
L32
            BT L33
            CLL OUTPUT
            BF L34
L34
L33
            BT L31
            SET
            BE
            LB
            CL 'L'
            GN
            NL
L30
L35


    def rule_EX1(self):
        rname = "EX1"
        rlabel = 0
            CLL EX2
            BF L36
L37
            TST '|'
            BF L38
            TB
            CL 'BT L'
            GN
            NL
            CLL EX2
            BE
L38
L39
            BT L37
            SET
            BE
            LB
            CL 'L'
            GN
            NL
L36
L40



