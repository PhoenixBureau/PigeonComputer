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

            self.LB()
            self.CL('class ')
            self.CI()
            self.CL('_compiler:')
            self.NL()
            self.LMI()
            self.NL()
            self.CL('def compile(self, source):')
            self.LMI()
            self.NL()
            self.CL('self.inbuf = source')
            self.NL()
            self.CL('self.pos = 0')
            self.NL()
            self.CL('self.outbuf = ""')
            self.NL()
            self.CL('self.margin = 0')
            self.NL()
            self.CL('self.gnlabel = 1')
            self.NL()
            self.CL('self.rule_')
            self.CI()
            self.CL('()')
            self.NL()
            self.CL('return self.outbuf')
            self.LMD()
            self.NL()
            self.NL()
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
            self.CL('def rule_')
            self.CI()
            self.CL('(self):')
            self.LMI()
            self.NL()
            self.CL('rname = "')
            self.CI()
            self.CL('"')
            self.NL()
            self.CL('rlabel = 0')
            self.NL()
            self.TST('→')
            if not flag: runBEjsfn(rname)

            self.rule_EX1()
            if not flag: runBEjsfn(rname)

            self.TST('▪')
            if not flag: runBEjsfn(rname)

            self.LMD()
            self.NL()
            self.NL()



    def rule_EX1(self):
        rname = "EX1"
        rlabel = 0
        self.rule_EX2()
        if flag:
            self.SET()
            while flag:
                self.TST('|')
                if flag:
                    self.CL('if not flag:')
                    self.LMI()
                    self.NL()
                    self.rule_EX2()
                    if not flag: runBEjsfn(rname)

                    self.LMD()
                    self.NL()


            self.SET()
            if not flag: runBEjsfn(rname)




    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
        self.rule_EX3()
        if flag:
            self.CL('if flag:')
            self.LMI()
            self.NL()

        if not flag:
            self.rule_OUTPUT()
            if flag:
                self.CL('if True:')
                self.LMI()
                self.NL()


        if flag:
            self.SET()
            while flag:
                self.rule_EX3()
                if flag:
                    self.CL('if not flag: runBEjsfn(rname)')
                    self.NL()
                    self.NL()

                if not flag:
                    self.rule_OUTPUT()
                    if flag:



            self.SET()
            if not flag: runBEjsfn(rname)

            self.LMD()
            self.NL()



    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
        self.ID()
        if flag:
            self.CL('self.rule_')
            self.CI()
            self.CL('()')
            self.NL()

        if not flag:
            self.SR()
            if flag:
                self.CL('self.TST(')
                self.CI()
                self.CL(')')
                self.NL()


        if not flag:
            self.TST('●')
            if flag:
                self.CL('self.ID()')
                self.NL()


        if not flag:
            self.TST('ℕ')
            if flag:
                self.CL('self.NUM()')
                self.NL()


        if not flag:
            self.TST('≋')
            if flag:
                self.CL('self.SR()')
                self.NL()


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
                self.CL('self.SET()')
                self.NL()


        if not flag:
            self.TST('★')
            if flag:
                self.CL('self.SET()')
                self.NL()
                self.CL('while flag:')
                self.LMI()
                self.NL()
                self.rule_EX3()
                if not flag: runBEjsfn(rname)

                self.LMD()
                self.NL()
                self.CL('self.SET()')
                self.NL()




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




    def rule_OUT1(self):
        rname = "OUT1"
        rlabel = 0
        self.TST('⊙')
        if flag:
            self.CL('self.CI()')
            self.NL()

        if not flag:
            self.SR()
            if flag:
                self.CL('self.CL(')
                self.CI()
                self.CL(')')
                self.NL()


        if not flag:
            self.TST('#')
            if flag:
                self.CL('if rlabel == 0:')
                self.LMI()
                self.NL()
                self.CL('rlable = self.gnlabel')
                self.NL()
                self.CL('self.gnlabel += 1')
                self.LMD()
                self.NL()
                self.CL('self.CL(str(rlabel))')
                self.NL()


        if not flag:
            self.TST('↵')
            if flag:
                self.CL('self.NL()')
                self.NL()


        if not flag:
            self.TST('⇤')
            if flag:
                self.CL('self.LB()')
                self.NL()


        if not flag:
            self.TST('⇥')
            if flag:
                self.CL('self.TB()')
                self.NL()


        if not flag:
            self.TST('↦')
            if flag:
                self.CL('self.LMI()')
                self.NL()


        if not flag:
            self.TST('↤')
            if flag:
                self.CL('self.LMD()')
                self.NL()





