from metaii_base import MetaII

class Compiler(MetaII):

    def compile(self, source):
        self.input = source
        self.reset()
        self.rule_PROGRAM()
        return self.output.getvalue()

    def rule_OUT1(self):
        rname = "OUT1"
        rlabel = 0
        self.TST('⊙')
        if self.switch:
            self.TB()
            self.CL('CI')
            self.NL()
            pass

        if not self.switch:
            self.SR()
            if self.switch:
                self.TB()
                self.CL('CL ')
                self.CI()
                self.NL()
                pass


        if not self.switch:
            self.TST('#')
            if self.switch:
                self.TB()
                self.CL('GN')
                self.NL()
                pass


        if not self.switch:
            self.TST('↵')
            if self.switch:
                self.TB()
                self.CL('NL')
                self.NL()
                pass


        if not self.switch:
            self.TST('⇤')
            if self.switch:
                self.TB()
                self.CL('LB')
                self.NL()
                pass


        if not self.switch:
            self.TST('⇥')
            if self.switch:
                self.TB()
                self.CL('TB')
                self.NL()
                pass


        if not self.switch:
            self.TST('↦')
            if self.switch:
                self.TB()
                self.CL('LMI')
                self.NL()
                pass


        if not self.switch:
            self.TST('↤')
            if self.switch:
                self.TB()
                self.CL('LMD')
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



    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
        self.ID()
        if self.switch:
            self.TB()
            self.CL('CLL ')
            self.CI()
            self.NL()
            pass

        if not self.switch:
            self.SR()
            if self.switch:
                self.TB()
                self.CL('TST ')
                self.CI()
                self.NL()
                pass


        if not self.switch:
            self.TST('●')
            if self.switch:
                self.TB()
                self.CL('ID')
                self.NL()
                pass


        if not self.switch:
            self.TST('ℕ')
            if self.switch:
                self.TB()
                self.CL('NUM')
                self.NL()
                pass


        if not self.switch:
            self.TST('≋')
            if self.switch:
                self.TB()
                self.CL('SR')
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
                self.TB()
                self.CL('SET')
                self.NL()
                pass


        if not self.switch:
            self.TST('★')
            if self.switch:
                self.LB()
                self.CL('L')
                if rlabel == 0:
                    rlable = self.gnlabel
                    self.gnlabel += 1
                self.CL(str(rlabel))
                self.NL()
                self.rule_EX3()
                if not self.switch: self.runBEjsfn(rname)

                self.TB()
                self.CL('BT L')
                if rlabel == 0:
                    rlable = self.gnlabel
                    self.gnlabel += 1
                self.CL(str(rlabel))
                self.NL()
                self.TB()
                self.CL('SET')
                self.NL()
                pass




    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
        self.rule_EX3()
        if self.switch:
            self.TB()
            self.CL('BF L')
            if rlabel == 0:
                rlable = self.gnlabel
                self.gnlabel += 1
            self.CL(str(rlabel))
            self.NL()
            pass

        if not self.switch:
            self.rule_OUTPUT()
            if self.switch:
                pass


        if self.switch:
            self.SET()
            while self.switch:
                self.rule_EX3()
                if self.switch:
                    self.TB()
                    self.CL('BE')
                    self.NL()
                    pass

                if not self.switch:
                    self.rule_OUTPUT()
                    if self.switch:
                        pass



            self.SET()
            if not self.switch: self.runBEjsfn(rname)

            self.LB()
            self.CL('L')
            if rlabel == 0:
                rlable = self.gnlabel
                self.gnlabel += 1
            self.CL(str(rlabel))
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
                    self.TB()
                    self.CL('BT L')
                    if rlabel == 0:
                        rlable = self.gnlabel
                        self.gnlabel += 1
                    self.CL(str(rlabel))
                    self.NL()
                    self.rule_EX2()
                    if not self.switch: self.runBEjsfn(rname)

                    pass


            self.SET()
            if not self.switch: self.runBEjsfn(rname)

            self.LB()
            self.CL('L')
            if rlabel == 0:
                rlable = self.gnlabel
                self.gnlabel += 1
            self.CL(str(rlabel))
            self.NL()
            pass



    def rule_ST(self):
        rname = "ST"
        rlabel = 0
        self.ID()
        if self.switch:
            self.LB()
            self.CI()
            self.NL()
            self.TST('→')
            if not self.switch: self.runBEjsfn(rname)

            self.rule_EX1()
            if not self.switch: self.runBEjsfn(rname)

            self.TST('▪')
            if not self.switch: self.runBEjsfn(rname)

            self.TB()
            self.CL('R')
            self.NL()
            pass



    def rule_PROGRAM(self):
        rname = "PROGRAM"
        rlabel = 0
        self.TST('▶')
        if self.switch:
            self.ID()
            if not self.switch: self.runBEjsfn(rname)

            self.LB()
            self.TB()
            self.CL('ADR ')
            self.CI()
            self.NL()
            self.SET()
            while self.switch:
                self.rule_ST()

            self.SET()
            if not self.switch: self.runBEjsfn(rname)

            self.TST('◀')
            if not self.switch: self.runBEjsfn(rname)

            self.TB()
            self.CL('END')
            self.NL()
            pass





if __name__ == "__main__":
    import sys
    c = Compiler()
    #source = sys.stdin.read()
    source = open('newlang5.newlang5', 'r').read()
    out = c.compile(source)
    print(out)

