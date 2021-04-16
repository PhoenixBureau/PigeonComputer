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


    def rule_ST(self):
        rname = "ST"
        rlabel = 0
            ID
            BF L3
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
L3


    def rule_EX1(self):
        rname = "EX1"
        rlabel = 0
            CLL EX2
            BF L4
L5
            TST '|'
            BF L6
            CL 'if not flag:'
            LMI
            NL
            CLL EX2
            BE
            LMD
            NL
L6
            BT L5
            SET
            BE
L4


    def rule_OUT1(self):
        rname = "OUT1"
        rlabel = 0
            TST '⊙'
            BF L7
            TB
            CL 'CI'
            NL
L7
        if not flag:
                SR
                BF L8
                TB
                CL 'CL '
                CI
                NL
L8

        if not flag:
                TST '#'
                BF L9
                TB
                CL 'GN'
                NL
L9

        if not flag:
                TST '↵'
                BF L10
                TB
                CL 'NL'
                NL
L10

        if not flag:
                TST '⇤'
                BF L11
                TB
                CL 'LB'
                NL
L11

        if not flag:
                TST '⇥'
                BF L12
                TB
                CL 'TB'
                NL
L12

        if not flag:
                TST '↦'
                BF L13
                TB
                CL 'LMI'
                NL
L13

        if not flag:
                TST '↤'
                BF L14
                TB
                CL 'LMD'
                NL
L14



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


    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
            ID
            BF L17
            TB
            CL 'CLL '
            CI
            NL
L17
        if not flag:
                SR
                BF L18
                TB
                CL 'TST '
                CI
                NL
L18

        if not flag:
                TST '●'
                BF L19
                TB
                CL 'ID'
                NL
L19

        if not flag:
                TST 'ℕ'
                BF L20
                TB
                CL 'NUM'
                NL
L20

        if not flag:
                TST '≋'
                BF L21
                TB
                CL 'SR'
                NL
L21

        if not flag:
                TST '('
                BF L22
                CLL EX1
                BE
                TST ')'
                BE
L22

        if not flag:
                TST '∅'
                BF L23
                TB
                CL 'SET'
                NL
L23

        if not flag:
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



    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
            CLL EX3
            BF L25
            TB
            CL 'BF L'
            GN
            NL
L25
        if not flag:
                CLL OUTPUT
                BF L26
L26

            BF L27
L28
            CLL EX3
            BF L29
            TB
            CL 'BE'
            NL
L29
        if not flag:
                CLL OUTPUT
                BF L30
L30

            BT L28
            SET
            BE
            LB
            CL 'L'
            GN
            NL
L27



