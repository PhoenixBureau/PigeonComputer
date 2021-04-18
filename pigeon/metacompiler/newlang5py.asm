    ADR PROGRAM
PROGRAM
    TST '▶'
    BF L1
    ID
    BE
    LB
    CL 'from metaii_base import MetaII'
    NL
    NL
    CL 'class Compiler(MetaII):'
    NL
    LMI
    NL
    CL 'def compile(self, source):'
    LMI
    NL
    CL 'self.input = source'
    NL
    CL 'self.reset()'
    NL
    CL 'self.rule_'
    CI
    CL '()'
    NL
    CL 'return self.output.getvalue()'
    LMD
    NL
    NL
L2
    CLL ST
    BT L2
    SET
    BE
    LMD
    NL
    NL
    CL 'if __name__ == "__main__":'
    LMI
    NL
    CL 'import sys'
    NL
    CL 'c = Compiler()'
    NL
    CL 'source = sys.stdin.read()'
    NL
    CL 'out = c.compile(source)'
    NL
    CL 'print(out)'
    LMD
    NL
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
    CL 'if not self.switch:'
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
EX2
    CLL EX3
    BF L11
    CL 'if self.switch:'
    LMI
    NL
L11
    BT L12
    CLL OUTPUT
    BF L13
    CL 'if True:'
    LMI
    NL
L13
L12
    BF L14
L15
    CLL EX3
    BF L16
    CL 'if not self.switch: self.runBEjsfn(rname)'
    NL
    NL
L16
    BT L17
    CLL OUTPUT
    BF L18
L18
L17
    BT L15
    SET
    BE
    CL 'pass'
    NL
    LMD
    NL
L14
L19
    R
EX3
    ID
    BF L20
    CL 'self.rule_'
    CI
    CL '()'
    NL
L20
    BT L21
    SR
    BF L22
    CL 'self.TST('
    CI
    CL ')'
    NL
L22
    BT L21
    TST '●'
    BF L23
    CL 'self.ID()'
    NL
L23
    BT L21
    TST 'ℕ'
    BF L24
    CL 'self.NUM()'
    NL
L24
    BT L21
    TST '≋'
    BF L25
    CL 'self.SR()'
    NL
L25
    BT L21
    TST '('
    BF L26
    CLL EX1
    BE
    TST ')'
    BE
L26
    BT L21
    TST '∅'
    BF L27
    CL 'self.switch = True'
    NL
L27
    BT L21
    TST '★'
    BF L28
    CL 'self.switch = True'
    NL
    CL 'while self.switch:'
    LMI
    NL
    CLL EX3
    BE
    LMD
    NL
    CL 'self.switch = True'
    NL
L28
L21
    R
OUTPUT
    TST '«'
    BF L29
L30
    CLL OUT1
    BT L30
    SET
    BE
    TST '»'
    BE
L29
L31
    R
OUT1
    TST '⊙'
    BF L32
    CL 'self.output_buffer += self.last'
    NL
L32
    BT L33
    SR
    BF L34
    CL 'self.output_buffer += '
    CI
    NL
L34
    BT L33
    TST '#'
    BF L35
    CL 'if rlabel == 0:'
    LMI
    NL
    CL 'rlabel = self.gnlabel'
    NL
    CL 'self.gnlabel += 1'
    LMD
    NL
    CL 'self.output_buffer += str(rlabel)'
    NL
L35
    BT L33
    TST '↵'
    BF L36
    CL 'print(self.output_buffer.rstrip(), file=self.output)'
    NL
    CL 'self.output_buffer = self._indent * self.indent'
    NL
L36
    BT L33
    TST '⇤'
    BF L37
    CL 'self.output_buffer = ""'
    NL
L37
    BT L33
    TST '⇥'
    BF L38
    CL 'self.output_buffer += self._indent'
    NL
L38
    BT L33
    TST '↦'
    BF L39
    CL 'self.indent += 1'
    NL
L39
    BT L33
    TST '↤'
    BF L40
    CL 'self.indent -= 1'
    NL
L40
L33
    R
    END

