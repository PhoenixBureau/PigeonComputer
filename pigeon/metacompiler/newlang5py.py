from metaii_base import MetaII

class Compiler(MetaII):

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

            self.output_buffer = ""
            self.output_buffer += 'from metaii_base import MetaII'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'class Compiler(MetaII):'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.indent += 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'def compile(self, source):'
            self.indent += 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'self.input = source'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'self.reset()'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'self.rule_'
            self.output_buffer += self.last
            self.output_buffer += '()'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'return self.output.getvalue()'
            self.indent -= 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.switch = True
            while self.switch:
                self.rule_ST()

            self.switch = True
            if not self.switch: self.runBEjsfn(rname)

            self.indent -= 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'if __name__ == "__main__":'
            self.indent += 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'import sys'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'c = Compiler()'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'source = sys.stdin.read()'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'out = c.compile(source)'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'print(out)'
            self.indent -= 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.TST('◀')
            if not self.switch: self.runBEjsfn(rname)

            pass



    def rule_ST(self):
        rname = "ST"
        rlabel = 0
        self.ID()
        if self.switch:
            self.output_buffer += 'def rule_'
            self.output_buffer += self.last
            self.output_buffer += '(self):'
            self.indent += 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'rname = "'
            self.output_buffer += self.last
            self.output_buffer += '"'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.output_buffer += 'rlabel = 0'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.TST('→')
            if not self.switch: self.runBEjsfn(rname)

            self.rule_EX1()
            if not self.switch: self.runBEjsfn(rname)

            self.TST('▪')
            if not self.switch: self.runBEjsfn(rname)

            self.indent -= 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass



    def rule_EX1(self):
        rname = "EX1"
        rlabel = 0
        self.rule_EX2()
        if self.switch:
            self.switch = True
            while self.switch:
                self.TST('|')
                if self.switch:
                    self.output_buffer += 'if not self.switch:'
                    self.indent += 1
                    print(self.output_buffer.rstrip(), file=self.output)
                    self.output_buffer = self._indent * self.indent
                    self.rule_EX2()
                    if not self.switch: self.runBEjsfn(rname)

                    self.indent -= 1
                    print(self.output_buffer.rstrip(), file=self.output)
                    self.output_buffer = self._indent * self.indent
                    pass


            self.switch = True
            if not self.switch: self.runBEjsfn(rname)

            pass



    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
        self.rule_EX3()
        if self.switch:
            self.output_buffer += 'if self.switch:'
            self.indent += 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass

        if not self.switch:
            self.rule_OUTPUT()
            if self.switch:
                self.output_buffer += 'if True:'
                self.indent += 1
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if self.switch:
            self.switch = True
            while self.switch:
                self.rule_EX3()
                if self.switch:
                    self.output_buffer += 'if not self.switch: self.runBEjsfn(rname)'
                    print(self.output_buffer.rstrip(), file=self.output)
                    self.output_buffer = self._indent * self.indent
                    print(self.output_buffer.rstrip(), file=self.output)
                    self.output_buffer = self._indent * self.indent
                    pass

                if not self.switch:
                    self.rule_OUTPUT()
                    if self.switch:
                        pass



            self.switch = True
            if not self.switch: self.runBEjsfn(rname)

            self.output_buffer += 'pass'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.indent -= 1
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass



    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
        self.ID()
        if self.switch:
            self.output_buffer += 'self.rule_'
            self.output_buffer += self.last
            self.output_buffer += '()'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass

        if not self.switch:
            self.SR()
            if self.switch:
                self.output_buffer += 'self.TST('
                self.output_buffer += self.last
                self.output_buffer += ')'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('●')
            if self.switch:
                self.output_buffer += 'self.ID()'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('ℕ')
            if self.switch:
                self.output_buffer += 'self.NUM()'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('≋')
            if self.switch:
                self.output_buffer += 'self.SR()'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
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
                self.output_buffer += 'self.switch = True'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('★')
            if self.switch:
                self.output_buffer += 'self.switch = True'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.output_buffer += 'while self.switch:'
                self.indent += 1
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.rule_EX3()
                if not self.switch: self.runBEjsfn(rname)

                self.indent -= 1
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.output_buffer += 'self.switch = True'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass




    def rule_OUTPUT(self):
        rname = "OUTPUT"
        rlabel = 0
        self.TST('«')
        if self.switch:
            self.switch = True
            while self.switch:
                self.rule_OUT1()

            self.switch = True
            if not self.switch: self.runBEjsfn(rname)

            self.TST('»')
            if not self.switch: self.runBEjsfn(rname)

            pass



    def rule_OUT1(self):
        rname = "OUT1"
        rlabel = 0
        self.TST('⊙')
        if self.switch:
            self.output_buffer += 'self.output_buffer += self.last'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass

        if not self.switch:
            self.SR()
            if self.switch:
                self.output_buffer += 'self.output_buffer += '
                self.output_buffer += self.last
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('#')
            if self.switch:
                self.output_buffer += 'if rlabel == 0:'
                self.indent += 1
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.output_buffer += 'rlabel = self.gnlabel'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.output_buffer += 'self.gnlabel += 1'
                self.indent -= 1
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.output_buffer += 'self.output_buffer += str(rlabel)'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('↵')
            if self.switch:
                self.output_buffer += 'print(self.output_buffer.rstrip(), file=self.output)'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.output_buffer += 'self.output_buffer = self._indent * self.indent'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('⇤')
            if self.switch:
                self.output_buffer += 'self.output_buffer = ""'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('⇥')
            if self.switch:
                self.output_buffer += 'self.output_buffer += self._indent'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('↦')
            if self.switch:
                self.output_buffer += 'self.indent += 1'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


        if not self.switch:
            self.TST('↤')
            if self.switch:
                self.output_buffer += 'self.indent -= 1'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass






if __name__ == "__main__":
    import sys
    c = Compiler()
    source = sys.stdin.read()
    out = c.compile(source)
    print(out)

