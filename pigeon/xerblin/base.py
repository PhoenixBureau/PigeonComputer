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
Xerblin Base
=================================

This module builds a Xerblin system out of purely "Functional" parts.

An interpreter is represented by a two-tuple that holds a stack and a
dictionary.

The stack is a sort of linked list structure while the dictionary is a
BTree that maps string names to four kinds of entries:

Functions - These must accept an interpreter, modify it somehow, and
return the modified interpreter.  They are defined in the library
module.

Or, one of three kinds of tuple.  The kind of the tuple is indicated
by its first member, which is a handler function, and the rest of the
tuple consists in its body as indicated:

    (SEQUENCE HANDLER, func0, func1, func2)
    
    (BRANCH HANDLER, true_func, false_func)
    
    (LOOP HANDLER, func0, func1, func2)

where any of the functions can be themselves SEQ, BRANCH, LOOP, or
plain functions as described above.

Interpretation is done by means of an apply_func(interpreter, function)
function that knows how to deal with the above combo-word tuples as well
as library word functions.

The first three functions defined in this module are used to build
"combo" commands in the UI.  There are corresponding commands in the
library (NewSeqWord, NewLoopWord, and NewBranchWord) that build tuples
with these functions as the first item in the tuple.  When apply_func()
encounters these tuples the initial handler function is used to "run" the
other functions in the tuple.

The three functions are:

    handle_sequence

    handle_branch

    handle_loop

The apply_func() function is used by the handlers and the interpret()
function to "run" commands on the interpreter.

Code Documentation
^^^^^^^^^^^^^^^^^^

'''
from pigeon.xerblin.btree import get


def _pop_TOS(I):
    '''
    Pop the top item off the stack and return it with the
    modified interpreter
    '''
    # This is a helper function factored out from handle_branch() and
    # handle_loop() below.
    (TOS, stack), dictionary = I
    return TOS, (stack, dictionary)


# These three following functions process the three kinds of combo-words.

def handle_sequence(I, seq):
    '''
    Run a sequence and return the modified interpreter.
    '''
    for func in seq[1:]:
        I = apply_func(I, func)
    return I


def handle_branch(I, branch):
    '''
    Check TOS and do one thing or another depending.
    '''
    TOS, I = _pop_TOS(I)
    func = branch[(not TOS) + 1] # i.e. True = 1; False = 2
    return apply_func(I, func)


def handle_loop(I, loop):
    '''
    Check TOS and do body if it's true, repeat.
    '''
    while True:
        TOS, I = _pop_TOS(I)
        if not TOS:
            break
        I = handle_sequence(I, loop)
    return I


def apply_func(I, func):
    '''
    Given an interpreter and a function or combo-word tuple, apply the
    function or combo to the interpreter and return the modified
    interpreter.
    '''
    if isinstance(func, tuple):
        handler = func[0]
        I = handler(I, func)
    else:
        I = func(I)
    return I


# This is the main point of this module.  It implements the system with
# the help of the apply_func() function.
def interpret(I, command):
    '''
    Given an interpreter and a string command, interpret that string on
    the interpreter and return the modified interpreter.
    '''
    for word in command:

        # Is it an integer?
        try:
            literal = int(word)
        except ValueError:

            # Is it a float?
            try:
                literal = float(word)
            except ValueError:

                # Is it a string literal?
                if word.startswith('"') and word.endswith('"'):
                    literal = word[1:-1]

                # Nope, it must be a command word.
                else:
                    # Interpret the word.
                    func = get(I[1], word)
                    I = apply_func(I, func)
                    continue

        # A literal was found, push it onto the stack.
        I = (literal, I[0]), I[1]

    return I

