# Library
'''
Library of Words
=================================

'''
from pickle import dumps, loads
from xerblin.base import handle_sequence, handle_loop, handle_branch
from xerblin.btree import get, insert, items, fill_tree
from xerblin.stack import pop, push, pick_, iterStack


# Mark the current namespace contents.
_existing = set(dir())
_existing.add('_existing')


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

