# -*- coding: utf-8 -*-
#
#    Copyright © 2012 Simon Forman
#
#    This file is part of Pigeon Computer.
#
#    Pigeon Computer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pigeon Computer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pigeon Computer.  If not, see <http://www.gnu.org/licenses/>.
#
'''
Library of Words
=================================

'''
from pickle import dumps, loads
from pigeon.xerblin.base import handle_sequence, handle_loop, handle_branch, enstacken
from pigeon.xerblin.btree import get, insert, items, fill_tree
from pigeon.xerblin.stack import pop, push, pick_, iterStack
from pigeon.assembler.pyavrasm import assemble as assemble_raw
from pigeon.metacompiler.metaii import comp


# Mark the current namespace contents.
_existing = set(dir())
_existing.add('_existing')


def assemble((stack, dictionary)):
    '''
    Assemble the top item on the stack which should be a string of
    assembly source.
    '''
    source, stack = stack
    HEX = assemble_raw(source)
    return (HEX, stack), dictionary


def compile((stack, dictionary)):
    '''
    Use the machine description on the top of the stack to compile the
    source in second stack cell.
    '''
    machine, (source, stack) = stack
    obj = comp(source, machine)
    return (obj, stack), dictionary


# Stack chatter.

def dup((stack, dictionary)):
    '''
    "Duplicate" the top item on the stack.
    '''
    return (stack[0], stack), dictionary


def swap((stack, dictionary)):
    '''
    Reverse the order of the top two items on the stack.
    '''
    TOS, second, stack = pop(stack, 2)
    stack = push(stack, TOS, second)
    return stack, dictionary


def pick((stack, dictionary)):
    '''
    Takes a number from the stack, counts back that many items (starting
    from zero for the top item) and puts a "duplicate" of the item found
    on the top of the stack. (So pick with 0 on the stack is thte same as
    the command "dup".)
    '''
    TOS, stack = stack
    stack = pick_(stack, TOS)
    return stack, dictionary


def tuck((stack, dictionary)):
    '''
    Put a "duplicate" of the item on the top of the stack just under the
    second item on the stack. (I.e. top, second, top.)
    '''
    TOS, second, stack = pop(stack, 2)
    stack = push(stack, TOS, second, TOS)
    return stack, dictionary


def drop((stack, dictionary)):
    '''
    Remove the item on the top of the stack and discard it.
    '''
    return stack[1], dictionary


def over((stack, dictionary)):
    '''
    Put a "duplicate" of the second item down in the stack on the top of
    the stack. (I.e. second, top, second.)
    '''
    second = stack[1][0]
    return (second, stack), dictionary


# Programming words.

def lookup(interpreter):
    '''
    Given a name on the top of the stack, look up the named command in
    the dictionary and put it on the stack in place of the name.
    '''
    (name, stack), dictionary = interpreter
    word = get(dictionary, name)
    return (word, stack), dictionary


def inscribe((stack, dictionary)):
    '''
    Given a name string on the top of the stack and a "combo" command
    underneath it (see NewSeqWord, NewLoopWord, and NewBranchWord for how
    to make combo commands) "inscribe" the combo command into the
    dictionary under that name, replacing any previous command of that
    name.
    '''
    name, word, stack = pop(stack, 2)
    dictionary = insert(dictionary, name, word)
    return stack, dictionary


def NewSeqWord((stack, dictionary)):
    '''
    This command takes all the items on the stack and puts them into a
    tuple with the Sequence Handler function in front of them.

    The items on the stack should all be commands from the dictionary,
    either functions or combo commands.  You get these by using the
    "lookup" command on the names of the functions you want.

    Put the first command to run on the stack first, then the second, and
    so on, so that the last item to run is on the top of the stack when
    you run this command.
    '''
    words = tuple(reversed(list(iterStack(stack))))
    seq = (handle_sequence,) + words
    return (seq, ()), dictionary


def NewLoopWord((stack, dictionary)):
    '''
    This command takes all the items on the stack and puts them into a
    tuple with the Loop Handler function in front of them.

    A Loop consumes the top item on the stack, then depending on it's
    "truth" either runs the commands in its tuple and repeats if it's
    true or stops looping altogether if it's false.

    Put the first command to run on the stack first, then the second, and
    so on, so that the last item to run is on the top of the stack when
    you run this command.
    '''
    words = tuple(reversed(list(iterStack(stack))))
    loop = (handle_loop,) + words
    return (loop, ()), dictionary


def NewBranchWord((stack, dictionary)):
    '''
    Create a new Branch command word.  A branch consumes the top item on
    the stack and does one of two things depending on its "truth" value.
    Unlike Loops and Sequences which use all the items on the stack,
    Branch commands only take the top two items. The item on the top of
    the stack should be a function to use in case of "true" and the
    second should be a function to use for "false".
    '''
    true, false, stack = pop(stack, 2)
    branch = (handle_branch, true, false)
    stack = push(stack, branch)
    return stack, dictionary


def NewEnstackener((stack, dictionary)):
    stack = list(iterStack(stack))
    stack.append(enstacken)
    stack = tuple(reversed(stack))
    return (stack, ()), dictionary


# Math words.

def add((stack, dictionary)):
    '''
    Add the top two items on the stack and replace them with the sum.
    '''
    a, b, stack = pop(stack, 2)
    return (a + b, stack), dictionary


def sub((stack, dictionary)):
    '''
    Replace the top two items on the stack with the result of subtracting
    the top item from the second item.
    '''
    a, b, stack = pop(stack, 2)
    return (b - a, stack), dictionary


def mul((stack, dictionary)):
    '''
    Replace the top two items on the stack with the result of multiplying
    them together.
    '''
    a, b, stack = pop(stack, 2)
    return (a * b, stack), dictionary


# Pickling words.

def pickle(interpreter):
    '''
    Convert the current interpreter to a portable text format (called a
    "pickle".)
    '''
    stack, dictionary = interpreter
    p = dumps(interpreter)
    return (p, stack), dictionary


def unpickle(interpreter):
    '''
    Take a string "pickle" portable text representation of an interpreter
    and replace the current interpreter with it.
    '''
    stack = interpreter[0]
    return loads(stack[0])


# System words

def rebalance((stack, dictionary)):
    '''
    This "rebalances" a dictionary.  It makes it more efficient to access
    commands in the dictionary if you've added a lot of new ones.

    It's a good idea to use this command before creating a pickle to
    save so that the saved pickle's dictionary is already balanced.
    '''
    dictionary = fill_tree((), items(dictionary))
    return stack, dictionary


def view(interpreter):
    '''
    Pretty print the interpreter to stdout.
    '''
    from pprint import pprint as p
    p(interpreter)
    return interpreter


def listwords(interpreter):
    '''
    Print the list of words in the dictionary to stdout.
    '''
    dictionary = interpreter[1]
    for name, func in items(dictionary):
        print name
    print
    return interpreter


# Now extract all the library functions we just defined.
_word_names = set(dir()) - _existing


# Pull words from this list.
words = [
    (name, function)
    for name, function in locals().items()
    if name in _word_names
    ]

# Add some text "constants".
words.extend([

    ('metaii.metaii', (enstacken, '''\
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

''')),

    ('metaii.asm', (enstacken, '''\
	ADR PROGRAM
OUT1
	TST '*1'
	BF L1
	CL 'GN1'
	OUT
L1
	BT L2
	TST '*2'
	BF L3
	CL 'GN2'
	OUT
L3
	BT L2
	TST '*'
	BF L4
	CL 'CI'
	OUT
L4
	BT L2
	SR
	BF L5
	CL 'CL '
	CI
	OUT
L5
L2
	R
OUTPUT
	TST '.OUT'
	BF L6
	TST '('
	BE
L7
	CLL OUT1
	BT L7
	SET
	BE
	TST ')'
	BE
L6
	BT L8
	TST '.LABEL'
	BF L9
	CL 'LB'
	OUT
	CLL OUT1
	BE
L9
L8
	BF L10
	CL 'OUT'
	OUT
L10
L11
	R
EX3
	ID
	BF L12
	CL 'CLL '
	CI
	OUT
L12
	BT L13
	SR
	BF L14
	CL 'TST '
	CI
	OUT
L14
	BT L13
	TST '.ID'
	BF L15
	CL 'ID'
	OUT
L15
	BT L13
	TST '.NUMBER'
	BF L16
	CL 'NUM'
	OUT
L16
	BT L13
	TST '.STRING'
	BF L17
	CL 'SR'
	OUT
L17
	BT L13
	TST '('
	BF L18
	CLL EX1
	BE
	TST ')'
	BE
L18
	BT L13
	TST '.EMPTY'
	BF L19
	CL 'SET'
	OUT
L19
	BT L13
	TST '$'
	BF L20
	LB
	GN1
	OUT
	CLL EX3
	BE
	CL 'BT '
	GN1
	OUT
	CL 'SET'
	OUT
L20
L13
	R
EX2
	CLL EX3
	BF L21
	CL 'BF '
	GN1
	OUT
L21
	BT L22
	CLL OUTPUT
	BF L23
L23
L22
	BF L24
L25
	CLL EX3
	BF L26
	CL 'BE'
	OUT
L26
	BT L27
	CLL OUTPUT
	BF L28
L28
L27
	BT L25
	SET
	BE
	LB
	GN1
	OUT
L24
L29
	R
EX1
	CLL EX2
	BF L30
L31
	TST '|'
	BF L32
	CL 'BT '
	GN1
	OUT
	CLL EX2
	BE
L32
L33
	BT L31
	SET
	BE
	LB
	GN1
	OUT
L30
L34
	R
ST
	ID
	BF L35
	LB
	CI
	OUT
	TST '='
	BE
	CLL EX1
	BE
	TST ';'
	BE
	CL 'R'
	OUT
L35
L36
	R
PROGRAM
	TST '.SYNTAX'
	BF L37
	ID
	BE
	CL 'ADR '
	CI
	OUT
L38
	CLL ST
	BT L38
	SET
	BE
	TST '.END'
	BE
	CL 'END'
	OUT
L37
L39
	R
	END

''')),

    ('demo.a1', (enstacken, '''\
.SYNTAX OOOLALA

OOOLALA = HUH | 'jones' | foo | bar ;

HUH = gary 'smith' tuesday ;

tuesday = day ( night | .EMPTY ) | cake ;

.END
''')),

    ('a1.metaii', (enstacken, '''\
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
''')),

    ])

