    ADR PROGRAM
PROGRAM
    TST '▶'
    BF L1
    ID
    BE
    LB
    CL 'program(['
    LMI
    NL
    CL 'start('
    CI
    CL '),'
    NL
L2
    CLL ST
    BT L2
    SET
    BE
    TST '◀'
    BE
    CL 'end]).'
    NL
L1
L3
    R
ST
    ID
    BF L4
    CL 'subroutine('
    CI
    CL '),'
    NL
    TST '→'
    BE
    CLL EX1
    BE
    TST '▪'
    BE
    CL 'return,'
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
    CL 'if_switch_goto(L'
    GN
    CL '),'
    NL
    CLL EX2
    BE
L8
L9
    BT L7
    SET
    BE
    LB
    CL 'label(L'
    GN
    CL '),'
    NL
L6
L10
    R
EX2
    CLL EX3
    BF L11
    CL 'if_not_switch_goto(L'
    GN
    CL '),'
    NL
L11
    BT L12
    CLL OUTPUT
    BF L13
L13
L12
    BF L14
L15
    CLL EX3
    BF L16
    CL 'or_die,'
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
    LB
    CL 'label(L'
    GN
    CL '),'
    NL
L14
L19
    R
EX3
    ID
    BF L20
    CL 'call('
    CI
    CL '),'
    NL
L20
    BT L21
    SR
    BF L22
    CL 'match('
    CI
    CL '),'
    NL
L22
    BT L21
    TST '●'
    BF L23
    CL 'match_identifier,'
    NL
L23
    BT L21
    TST 'ℕ'
    BF L24
    CL 'match_number,'
    NL
L24
    BT L21
    TST '≋'
    BF L25
    CL 'match_string_literal,'
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
    CL 'set_switch,'
    NL
L27
    BT L21
    TST '★'
    BF L28
    LB
    CL 'label(L'
    GN
    CL '),'
    NL
    CLL EX3
    BE
    CL 'if_switch_goto(L'
    GN
    CL '),'
    NL
    CL 'set_switch,'
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
    CL 'copy_last_match,'
    NL
L32
    BT L33
    SR
    BF L34
    CL 'copy_literal('
    CI
    CL '),'
    NL
L34
    BT L33
    TST '#'
    BF L35
    CL 'generate_number,'
    NL
L35
    BT L33
    TST '↵'
    BF L36
    CL 'copy_newline,'
    NL
L36
    BT L33
    TST '⇤'
    BF L37
    CL 'reset_left_margin,'
    NL
L37
    BT L33
    TST '⇥'
    BF L38
    CL 'copy_tab,'
    NL
L38
    BT L33
    TST '↦'
    BF L39
    CL 'indent,'
    NL
L39
    BT L33
    TST '↤'
    BF L40
    CL 'dedent,'
    NL
L40
L33
    R
    END

