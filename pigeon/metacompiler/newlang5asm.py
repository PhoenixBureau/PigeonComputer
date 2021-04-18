from metaii_base import MetaII, ParseError


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
            self.output_buffer += self._indent
            self.output_buffer += 'CI'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass
        if not self.switch:
            self.SR()
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'CL '
                self.output_buffer += self.last
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('#')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'GN'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('↵')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'NL'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('⇤')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'LB'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('⇥')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'TB'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('↦')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'LMI'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('↤')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'LMD'
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
            if not self.switch:
                raise ParseError(rname)

            self.TST('»')
            if not self.switch:
                raise ParseError(rname)

            pass

    def rule_EX3(self):
        rname = "EX3"
        rlabel = 0
        self.ID()
        if self.switch:
            self.output_buffer += self._indent
            self.output_buffer += 'CLL '
            self.output_buffer += self.last
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass
        if not self.switch:
            self.SR()
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'TST '
                self.output_buffer += self.last
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('●')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'ID'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('ℕ')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'NUM'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('≋')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'SR'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('(')
            if self.switch:
                self.rule_EX1()
                if not self.switch:
                    raise ParseError(rname)

                self.TST(')')
                if not self.switch:
                    raise ParseError(rname)

                pass

        if not self.switch:
            self.TST('∅')
            if self.switch:
                self.output_buffer += self._indent
                self.output_buffer += 'SET'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass

        if not self.switch:
            self.TST('★')
            if self.switch:
                self.output_buffer = ""
                self.output_buffer += 'L'
                if rlabel == 0:
                    rlabel = self.gnlabel
                    self.gnlabel += 1
                self.output_buffer += str(rlabel)
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.rule_EX3()
                if not self.switch:
                    raise ParseError(rname)

                self.output_buffer += self._indent
                self.output_buffer += 'BT L'
                if rlabel == 0:
                    rlabel = self.gnlabel
                    self.gnlabel += 1
                self.output_buffer += str(rlabel)
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                self.output_buffer += self._indent
                self.output_buffer += 'SET'
                print(self.output_buffer.rstrip(), file=self.output)
                self.output_buffer = self._indent * self.indent
                pass


    def rule_EX2(self):
        rname = "EX2"
        rlabel = 0
        self.rule_EX3()
        if self.switch:
            self.output_buffer += self._indent
            self.output_buffer += 'BF L'
            if rlabel == 0:
                rlabel = self.gnlabel
                self.gnlabel += 1
            self.output_buffer += str(rlabel)
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass
        if not self.switch:
            self.rule_OUTPUT()
            if self.switch:
                pass

        if self.switch:
            self.switch = True
            while self.switch:
                self.rule_EX3()
                if self.switch:
                    self.output_buffer += self._indent
                    self.output_buffer += 'BE'
                    print(self.output_buffer.rstrip(), file=self.output)
                    self.output_buffer = self._indent * self.indent
                    pass
                if not self.switch:
                    self.rule_OUTPUT()
                    if self.switch:
                        pass


            self.switch = True
            if not self.switch:
                raise ParseError(rname)

            self.output_buffer = ""
            self.output_buffer += 'L'
            if rlabel == 0:
                rlabel = self.gnlabel
                self.gnlabel += 1
            self.output_buffer += str(rlabel)
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
                    self.output_buffer += self._indent
                    self.output_buffer += 'BT L'
                    if rlabel == 0:
                        rlabel = self.gnlabel
                        self.gnlabel += 1
                    self.output_buffer += str(rlabel)
                    print(self.output_buffer.rstrip(), file=self.output)
                    self.output_buffer = self._indent * self.indent
                    self.rule_EX2()
                    if not self.switch:
                        raise ParseError(rname)

                    pass

            self.switch = True
            if not self.switch:
                raise ParseError(rname)

            self.output_buffer = ""
            self.output_buffer += 'L'
            if rlabel == 0:
                rlabel = self.gnlabel
                self.gnlabel += 1
            self.output_buffer += str(rlabel)
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass

    def rule_ST(self):
        rname = "ST"
        rlabel = 0
        self.ID()
        if self.switch:
            self.output_buffer = ""
            self.output_buffer += self.last
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.TST('→')
            if not self.switch:
                raise ParseError(rname)

            self.rule_EX1()
            if not self.switch:
                raise ParseError(rname)

            self.TST('▪')
            if not self.switch:
                raise ParseError(rname)

            self.output_buffer += self._indent
            self.output_buffer += 'R'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass

    def rule_PROGRAM(self):
        rname = "PROGRAM"
        rlabel = 0
        self.TST('▶')
        if self.switch:
            self.ID()
            if not self.switch:
                raise ParseError(rname)

            self.output_buffer = ""
            self.output_buffer += self._indent
            self.output_buffer += 'ADR '
            self.output_buffer += self.last
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            self.switch = True
            while self.switch:
                self.rule_ST()

            self.switch = True
            if not self.switch:
                raise ParseError(rname)

            self.TST('◀')
            if not self.switch:
                raise ParseError(rname)

            self.output_buffer += self._indent
            self.output_buffer += 'END'
            print(self.output_buffer.rstrip(), file=self.output)
            self.output_buffer = self._indent * self.indent
            pass


if __name__ == "__main__":
    import sys
    c = Compiler()
    source = sys.stdin.read()
    out = c.compile(source)
    print(out)

