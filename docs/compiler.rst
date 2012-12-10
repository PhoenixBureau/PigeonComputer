
Pigeon Compiler
============================================


Simple Polymorphic Compiler
----------------------------


Meta-II (1964)
----------------------------

This is the (slightly modified FOOTNOTE) description of the Meta-II
self-regenerating compiler::

    .SYNTAX PROGRAM

    OUT1 = '*1' .OUT('GN1') |
           '*2' .OUT('GN2') |
           '*' .OUT('CI') |
           .STRING .OUT('CL '*) ;

    OUTPUT = ('.OUT' '(' $ OUT1 ')' |
              '.LABEL' .OUT('LB') OUT1)
             .OUT('OUT') ;

    EX3 = .ID .OUT('CLL '*) |
          .STRING .OUT('TST '*) |
          '.ID' .OUT('ID') |
          '.NUMBER' .OUT('NUM') |
          '.STRING' .OUT('SR') |
          '(' EX1 ')' |
          '.EMPTY' .OUT('SET') |
          '$' .LABEL *1 EX3 .OUT('BT ' *1) .OUT('SET') ;

    EX2 = (EX3 .OUT('BF ' *1) | OUTPUT) $ (EX3 .OUT('BE') | OUTPUT)
          .LABEL *1 ;

    EX1 = EX2 $('|' .OUT('BT ' *1) EX2 )
          .LABEL *1 ;

    ST = .ID .LABEL * '=' EX1 ';' .OUT('R') ;

    PROGRAM = '.SYNTAX' .ID .OUT('ADR ' *) $ ST '.END' .OUT('END') ;

    .END


The Meta-II engine compiles the above description into an assembly source
file (see `metaii.asm`_) which is *the same* assembly source file that
it uses to compile the assembly source file.

The assembly code regenerates itself.  (Where do you get it the first
time?  You must emulate the engine in your mind and compile it by hand,
or crib a copy from someone else.)

.. _metaii.asm: https://github.com/PhoenixBureau/PigeonComputer/blob/master/metacompiler/metaii.asm


.. automodule:: metaii


Language Design and Compiler Extentions
---------------------------------------

TODO: Write up a bit about all the myriad ways to go from here
(basically ALL THE REST OF COMPUTER PROGRAMMING!!) Lol.

For example, here is the Meta-II compiler description rewritten to target
the Pigeon Assembler::

    .SYNTAX PROGRAM

    OUT1 = '*1' .OUT('gen_label_1()') |
           '*2' .OUT('gen_label_2()') |
           '*' .OUT('copy_input()') |
           .STRING .OUT('copy_literal(' * ')') ;

    OUTPUT = ('.OUT' '(' $ OUT1 ')' |
              '.LABEL' .OUT('LB') OUT1)
             .OUT('output_line()') ;

    EX3 = .ID .OUT('call(' * ')') |
          .STRING .OUT('startswith(' * ')') |
          '.ID' .OUT('identifier()') |
          '.NUMBER' .OUT('number()') |
          '.STRING' .OUT('string()') |
          '(' EX1 ')' |
          '.EMPTY' .OUT('sbr(switch_reg, 1 << switch_bit)') |
          '$' .OUT('label(' *1 ')') EX3
           .OUT('sbrc(switch_reg, switch_bit)')
           .OUT('jmp(' *1 ')')
           .OUT('sbr(switch_reg, 1 << switch_bit)') ;

    EX2 = (EX3
            .OUT('sbrs(switch_reg, switch_bit)')
            .OUT('jmp(' *1 ')')
           | OUTPUT)
        $ (EX3
            .OUT('sbrs(switch_reg, switch_bit)')
            .OUT('jmp(ERROR)')
           | OUTPUT)
          .OUT('label(' *1 ')') ;

    EX1 = EX2 $('|'
                 .OUT('sbrc(switch_reg, switch_bit)')
                 .OUT('jmp(' *1 ')')
                EX2 )
          .OUT('label(' *1 ')') ;

    ST = .ID .OUT('label(' * ') # subroutine ==========')
           '=' EX1 ';' .OUT('ret()') .OUT('') ;

    PROGRAM = '.SYNTAX' .ID
                 .OUT('define(switch_bit=0)')
                 .OUT('define(switch_reg=r0)')
                 .OUT('')
                 .OUT('label(' * ')')
              $ ST '.END' .OUT('#END') ;

    .END


It's not super-useful as-is, but it demonstrates the idea.


