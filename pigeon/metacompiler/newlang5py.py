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
        self.TST('▶')
        if flag:
            self.ID()
            if not flag: runBEjsfn(rname)

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
            self.SET()
            while flag:
                self.rule_ST()

            self.SET()
            if not flag: runBEjsfn(rname)

            self.TST('◀')
            if not flag: runBEjsfn(rname)




    def rule_ST(self):
        rname = "ST"
        rlabel = 0
        self.ID()
        if flag:
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
            self.TST('→')
            if not flag: runBEjsfn(rname)

            self.rule_EX1()
            if not flag: runBEjsfn(rname)

            self.TST('▪')
            if not flag: runBEjsfn(rname)

                LMD
                NL
                NL



    def rule_EX1(self):
        rname = "EX1"
        rlabel = 0
        self.rule_EX2()
        if flag:
            self.SET()
            while flag:
                self.TST('|')
                if flag:
                        CL 'if not flag:'
                        LMI
                        NL
                    self.rule_EX2()
                    if not flag: runBEjsfn(rname)

                        LMD
                        NL


            self.SET()
            if not flag: runBEjsfn(rname)




    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
        self.rule_EX3()
        if flag:
                CL 'if flag:'
                LMI
                NL

        if not flag:
            self.rule_OUTPUT()
            if flag:
                    CL 'if True:'
                    LMI
                    NL


        if flag:
            self.SET()
            while flag:
                self.rule_EX3()
                if flag:
                        CL 'if not flag: runBEjsfn(rname)'
                        NL
                        NL

                if not flag:
                    self.rule_OUTPUT()
                    if flag:



            self.SET()
            if not flag: runBEjsfn(rname)

                LMD
                NL



    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
        self.ID()
        if flag:
                CL 'self.rule_'
                CI
                CL '()'
                NL

        if not flag:
            self.SR()
            if flag:
                    CL 'self.TST('
                    CI
                    CL ')'
                    NL


        if not flag:
            self.TST('●')
            if flag:
                    CL 'self.ID()'
                    NL


        if not flag:
            self.TST('ℕ')
            if flag:
                    CL 'self.NUM()'
                    NL


        if not flag:
            self.TST('≋')
            if flag:
                    CL 'self.SR()'
                    NL


        if not flag:
            self.TST('(')
            if flag:
                self.rule_EX1()
                if not flag: runBEjsfn(rname)

                self.TST(')')
                if not flag: runBEjsfn(rname)



        if not flag:
            self.TST('∅')
            if flag:
                    CL 'self.SET()'
                    NL


        if not flag:
            self.TST('★')
            if flag:
                    CL 'self.SET()'
                    NL
                    CL 'while flag:'
                    LMI
                    NL
                self.rule_EX3()
                if not flag: runBEjsfn(rname)

                    LMD
                    NL
                    CL 'self.SET()'
                    NL




    def rule_OUT1(self):
        rname = "OUT1"
        rlabel = 0
        self.TST('⊙')
        if flag:
                TB
                CL 'CI'
                NL

        if not flag:
            self.SR()
            if flag:
                    TB
                    CL 'CL '
                    CI
                    NL


        if not flag:
            self.TST('#')
            if flag:
                    TB
                    CL 'GN'
                    NL


        if not flag:
            self.TST('↵')
            if flag:
                    TB
                    CL 'NL'
                    NL


        if not flag:
            self.TST('⇤')
            if flag:
                    TB
                    CL 'LB'
                    NL


        if not flag:
            self.TST('⇥')
            if flag:
                    TB
                    CL 'TB'
                    NL


        if not flag:
            self.TST('↦')
            if flag:
                    TB
                    CL 'LMI'
                    NL


        if not flag:
            self.TST('↤')
            if flag:
                    TB
                    CL 'LMD'
                    NL




    def rule_OUTPUT(self):
        rname = "OUTPUT"
        rlabel = 0
        self.TST('«')
        if flag:
            self.SET()
            while flag:
                self.rule_OUT1()

            self.SET()
            if not flag: runBEjsfn(rname)

            self.TST('»')
            if not flag: runBEjsfn(rname)





