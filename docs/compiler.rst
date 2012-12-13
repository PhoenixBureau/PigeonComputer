
Pigeon Compiler
============================================

In order to teach the basics of compilers and the compilation process
there is a simple but very flexible and powerful *meta-compiler* built
around a fascinating 1964 paper/project/artifact `Meta-II`_.

.. _Meta-II: http://en.wikipedia.org/wiki/META_II

Simple Polymorphic Compiler
----------------------------

Tiny engine that loads and runs *compiler descriptions* which then allow
it to become several different compilers (including a compiler which can
compile itself which is why it's called a "meta-compiler".)

A simple high-level description like this::

    .SYNTAX OOOLALA

    OOOLALA = HUH | 'jones' | foo | bar ;

    HUH = gary 'smith' tuesday ;

    tuesday = day ( night | .EMPTY ) | cake ;

    .END

...gets compiled into this assembly code::

    # Program OOOLALA
    # (preamble)
    set_switch()

    label(OOOLALA) # subroutine ==========
    call(HUH)
    if_not_switch_jmp_to(L1)
    label(L1)
    if_switch_jmp_to(L2)
    expect('jones')
    if_not_switch_jmp_to(L3)
    label(L3)
    if_switch_jmp_to(L2)
    call(foo)
    if_not_switch_jmp_to(L4)
    label(L4)
    if_switch_jmp_to(L2)
    call(bar)
    if_not_switch_jmp_to(L5)
    label(L5)
    label(L2)
    ret()

    label(HUH) # subroutine ==========
    call(gary)
    if_not_switch_jmp_to(L6)
    expect('smith')
    if_not_switch_jmp_to(ERROR)
    call(tuesday)
    if_not_switch_jmp_to(ERROR)
    label(L6)
    label(L7)
    ret()

    label(tuesday) # subroutine ==========
    call(day)
    if_not_switch_jmp_to(L8)
    call(night)
    if_not_switch_jmp_to(L9)
    label(L9)
    if_switch_jmp_to(L10)
    set_switch()
    if_not_switch_jmp_to(L11)
    label(L11)
    label(L10)
    if_not_switch_jmp_to(ERROR)
    label(L8)
    if_switch_jmp_to(L12)
    call(cake)
    if_not_switch_jmp_to(L13)
    label(L13)
    label(L12)
    ret()

    #END


Val Shorre’s Meta-II Metacompiler
---------------------------------

The Meta-II engine compiles the `metaii.metaii`_ description into an assembly source
file (see `metaii.asm`_) which is *the same* assembly source file that
it uses to compile the assembly source file.

The assembly code regenerates itself.  (Where do you get it the first
time?  You must emulate the engine in your mind and compile it by hand,
or crib a copy from someone else.)

.. _metaii.asm: https://github.com/PhoenixBureau/PigeonComputer/blob/master/metacompiler/metaii.asm

.. _metaii.metaii: https://github.com/PhoenixBureau/PigeonComputer/blob/master/metacompiler/metaii.metaii

Here is the documentation on the Meta-II engine included in the Pigeon Computer project:

.. automodule:: metaii


Language Design and Compiler Extentions
---------------------------------------

TODO: Write up a bit about all the myriad ways to go from here
(basically ALL THE REST OF COMPUTER PROGRAMMING!!) Lol.

For example, here is the Meta-II compiler description that compiles the
above high-level source to target the Pigeon Assembler::

    .SYNTAX PROGRAM

    EX3 = .ID .OUT('call(' * ')') |
          .STRING .OUT('expect(' * ')') |
          '(' EX1 ')' |
          '.EMPTY' .OUT('set_switch()') |

          '$' .OUT('label(' *1 ')')
          EX3 .OUT('if_switch_jmp_to(' *1 ')')
              .OUT('set_switch()') ;

    EX2 = (EX3 .OUT('if_not_switch_jmp_to(' *1 ')'))
          $ (EX3 .OUT('if_not_switch_jmp_to(ERROR)'))
          .OUT('label(' *1 ')') ;

    EX1 = EX2 $ ( '|' .OUT('if_switch_jmp_to(' *1 ')') EX2)
          .OUT('label(' *1 ')') ;

    ST = .ID .OUT('label(' * ') # subroutine ==========')
         '='
         EX1
         ';' .OUT('ret()') .OUT('') ;

    PROGRAM = '.SYNTAX'
              .ID .OUT('# Program ' * )
                  .OUT('# (preamble)')
                  .OUT('set_switch()')
                  .OUT('')
              $ ST
              '.END' .OUT('#END') ;

    .END

