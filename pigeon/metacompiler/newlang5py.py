from metaii_base import MetaII

class PROGRAM_compiler(MetaII):

    def compile(self, source):
        self.input = source
        self.reset()
        self.rule_PROGRAM()
        return self.output.getvalue()

    def rule_PROGRAM(self):
        rname = "PROGRAM"
        rlabel = 0
        self.TST('▶')
        if self.switch:
            self.ID()
            if not self.switch: self.runBEjsfn(rname)

            self.LB()
            self.CL('from metaii_base import MetaII')
            self.NL()
            self.NL()
            self.CL('class ')
            self.CI()
            self.CL('_compiler(MetaII):')
            self.NL()
            self.LMI()
            self.NL()
            self.CL('def compile(self, source):')
            self.LMI()
            self.NL()
            self.CL('self.input = source')
            self.NL()
            self.CL('self.reset()')
            self.NL()
            self.CL('self.rule_')
            self.CI()
            self.CL('()')
            self.NL()
            self.CL('return self.output.getvalue()')
            self.LMD()
            self.NL()
            self.NL()
            self.SET()
            while self.switch:
                self.rule_ST()

            self.SET()
            if not self.switch: self.runBEjsfn(rname)

            self.TST('◀')
            if not self.switch: self.runBEjsfn(rname)

            pass



    def rule_ST(self):
        rname = "ST"
        rlabel = 0
        self.ID()
        if self.switch:
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
            if not self.switch: self.runBEjsfn(rname)

            self.rule_EX1()
            if not self.switch: self.runBEjsfn(rname)

            self.TST('▪')
            if not self.switch: self.runBEjsfn(rname)

            self.LMD()
            self.NL()
            self.NL()
            pass



    def rule_EX1(self):
        rname = "EX1"
        rlabel = 0
        self.rule_EX2()
        if self.switch:
            self.SET()
            while self.switch:
                self.TST('|')
                if self.switch:
                    self.CL('if not self.switch:')
                    self.LMI()
                    self.NL()
                    self.rule_EX2()
                    if not self.switch: self.runBEjsfn(rname)

                    self.LMD()
                    self.NL()
                    pass


            self.SET()
            if not self.switch: self.runBEjsfn(rname)

            pass



    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
        self.rule_EX3()
        if self.switch:
            self.CL('if self.switch:')
            self.LMI()
            self.NL()
            pass

        if not self.switch:
            self.rule_OUTPUT()
            if self.switch:
                self.CL('if True:')
                self.LMI()
                self.NL()
                pass


        if self.switch:
            self.SET()
            while self.switch:
                self.rule_EX3()
                if self.switch:
                    self.CL('if not self.switch: self.runBEjsfn(rname)')
                    self.NL()
                    self.NL()
                    pass

                if not self.switch:
                    self.rule_OUTPUT()
                    if self.switch:
                        pass



            self.SET()
            if not self.switch: self.runBEjsfn(rname)

            self.CL('pass')
            self.NL()
            self.LMD()
            self.NL()
            pass



    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
        self.ID()
        if self.switch:
            self.CL('self.rule_')
            self.CI()
            self.CL('()')
            self.NL()
            pass

        if not self.switch:
            self.SR()
            if self.switch:
                self.CL('self.TST(')
                self.CI()
                self.CL(')')
                self.NL()
                pass


        if not self.switch:
            self.TST('●')
            if self.switch:
                self.CL('self.ID()')
                self.NL()
                pass


        if not self.switch:
            self.TST('ℕ')
            if self.switch:
                self.CL('self.NUM()')
                self.NL()
                pass


        if not self.switch:
            self.TST('≋')
            if self.switch:
                self.CL('self.SR()')
                self.NL()
                pass


        if not self.switch:
            self.TST('(')
            if self.switch:
                self.rule_EX1()
                if not self.switch: self.runBEjsfn(rname)

                self.TST(')')
                if not self.switch: self.runBEjsfn(rname)

                pass


        if not self.switch:
            self.TST('∅')
            if self.switch:
                self.CL('self.SET()')
                self.NL()
                pass


        if not self.switch:
            self.TST('★')
            if self.switch:
                self.CL('self.SET()')
                self.NL()
                self.CL('while self.switch:')
                self.LMI()
                self.NL()
                self.rule_EX3()
                if not self.switch: self.runBEjsfn(rname)

                self.LMD()
                self.NL()
                self.CL('self.SET()')
                self.NL()
                pass




    def rule_OUTPUT(self):
        rname = "OUTPUT"
        rlabel = 0
        self.TST('«')
        if self.switch:
            self.SET()
            while self.switch:
                self.rule_OUT1()

            self.SET()
            if not self.switch: self.runBEjsfn(rname)

            self.TST('»')
            if not self.switch: self.runBEjsfn(rname)

            pass



    def rule_OUT1(self):
        rname = "OUT1"
        rlabel = 0
        self.TST('⊙')
        if self.switch:
            self.CL('self.CI()')
            self.NL()
            pass

        if not self.switch:
            self.SR()
            if self.switch:
                self.CL('self.CL(')
                self.CI()
                self.CL(')')
                self.NL()
                pass


        if not self.switch:
            self.TST('#')
            if self.switch:
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
                pass


        if not self.switch:
            self.TST('↵')
            if self.switch:
                self.CL('self.NL()')
                self.NL()
                pass


        if not self.switch:
            self.TST('⇤')
            if self.switch:
                self.CL('self.LB()')
                self.NL()
                pass


        if not self.switch:
            self.TST('⇥')
            if self.switch:
                self.CL('self.TB()')
                self.NL()
                pass


        if not self.switch:
            self.TST('↦')
            if self.switch:
                self.CL('self.LMI()')
                self.NL()
                pass


        if not self.switch:
            self.TST('↤')
            if self.switch:
                self.CL('self.LMD()')
                self.NL()
                pass





