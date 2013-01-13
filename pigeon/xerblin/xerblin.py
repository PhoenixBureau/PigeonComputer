# -*- coding: utf-8 -*-
#
#    Copyright © 2013 Simon Forman
#
#    This file is Xerblin.
#
#    Xerblin is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Xerblin is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Xerblin.  If not, see <http://www.gnu.org/licenses/>.
#
import pickle, pprint, StringIO, os


'''
Stack
=================================

Tuple-based persistent stack.

This is too simple to document.  It's almost too simple to implement.
'''


def push(stack, *items):
    '''Push arguments onto a stack.'''
    for item in items:
        stack = item, stack # push
    return stack


def pop(stack, number):
    '''Pop number arguments from stack.'''
    for _ in range(number):
        item, stack = stack # pop
        yield item
    yield stack


def iterStack(stack):
    '''Iterate through the items on the stack.'''
    while stack:
        item, stack = stack
        yield item


def lenStack(stack):
    '''Return the number of items on the stack.'''
    return sum(1 for _ in iterStack(stack))


def pick_(stack, n):
    '''
    Find the nth item on the stack and duplicate it to TOS. (Pick with
    zero is the same as "dup".)
    '''
    if n < 0:
        raise ValueError
    s = stack
    while True:
        try:
            item, s = s
        except ValueError:
            raise IndexError
        n -= 1
        if n < 0:
            break
    return item, stack


'''
BTree
=================================

This is a simple Binary Tree implementation that uses tuples in such a
way as to permit "persistant" usage, i.e. all previous versions of the
btree datastructures are retained and available (provided you don't throw
them away yourself.)

The empty tree is represented as an empty tuple.  Nodes are a tuple
consisting of a key, a value, and two (possible empty) sub-nodes for the
lower and higher branches of the tree.

This module defines the following functions:

    insert(node, key, value)

    get(node, key)

    delete(node, key)

Both insert() and delete() return a new tuple that is the result of
applying the operation to the existing node.  (And both get() and delete()
will raise KeyErrors if the key is not in the tree.)

Because of the way that insert() and delete() are written, only as much
of the tree is changed as necessary and the rest of it is reused. This
provides persistance without using up memory for each version of the
tree.

These functions are implemented recursively so they have the potential to
raise a RuntimeError if the maximum recursion depth is exceeded.  This
should only be a problem if used with very large trees.  To avoid this
issue you can use sys.setrecursionlimit(), but I think I might just
rewrite these to not use recursion.
'''


def insert(node, key, value):
    '''
    Return a tree with value stored under key. Replaces old value if any.
    '''
    if not node:
        return key, value, (), ()

    node_key, node_value, lower, higher = node

    if key < node_key:
        return node_key, node_value, insert(lower, key, value), higher

    if key > node_key:
        return node_key, node_value, lower, insert(higher, key, value)

    return key, value, lower, higher


def get(node, key):
    '''
    Return the value stored under key or raise KeyError if not found.
    '''
    if not node:
        raise KeyError, key

    node_key, value, lower, higher = node

    if key == node_key:
        return value

    return get(lower if key < node_key else higher, key)


def delete(node, key):
    '''
    Return a tree with the value (and key) removed or raise KeyError if
    not found.
    '''
    if not node:
        raise KeyError, key

    node_key, value, lower, higher = node

    if key < node_key:
        return node_key, value, delete(lower, key), higher

    if key > node_key:
        return node_key, value, lower, delete(higher, key)

    # So, key == node_key, delete this node itself.

    # If we only have one non-empty child node return it.  If both child
    # nodes are empty return an empty node (one of the children.)
    if not lower:
        return higher
    if not higher:
        return lower

    # If both child nodes are non-empty, we find the highest node in our
    # lower sub-tree, take its key and value to replace (delete) our own,
    # then get rid of it by recursively calling delete() on our lower
    # sub-node with our new key.
    # (We could also find the lowest node in our higher sub-tree and take
    # its key and value and delete it. I only implemented one of these
    # two symmetrical options. Over a lot of deletions this might make
    # the tree more unbalanced.  Oh well.)
    node = lower
    while node[3]:
        node = node[3]
    key, value = node[:2]

    return key, value, delete(lower, key), higher


# The above functions are the "core" functionality for dealing with this
# tuple-based persistant BTree datastructure.  The rest of these are just
# helper functions.


def items(node):
    '''
    Iterate in order over the (key, value) pairs in a tree.
    '''
    if not node:
        return

    key, value, lower, higher = node
    
    for kv in items(lower):
        yield kv
    
    yield key, value
    
    for kv in items(higher):
        yield kv


def _yield_balanced(sorted_items):
    '''
    Recursive generator function to yield the items in a sorted sequence
    in such a way as to fill a btree in a balanced fashion.
    '''
    # For empty sequences do nothing.
    if not sorted_items:
        return

    # Find the index of the middle item (rounding down for even-length
    # sequences due to integer division.)
    i = len(sorted_items) / 2

    # Yield the middle item.
    yield sorted_items[i]

    # Shortcut in case len(sorted_items) == 1
    if not i:
        return 

    # Now recurse on lower and higher halves of the sequence.
    for low in _yield_balanced(sorted_items[:i]):
        yield low
    for high in _yield_balanced(sorted_items[i+1:]):
        yield high


def fill_tree(node, items):
    '''
    Add the (key, value) pairs in items to a btree in a balanced way.

    You can balance a tree like so:

        tree = fill_tree((), items(tree))

    This iterates through the tree and returns a new, balanced tree from
    its contents.
    '''
    for key, value in _yield_balanced(sorted(items)):
        node = insert(node, key, value)
    return node


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

    (handle_sequence, func0, func1, func2, ...)

    (handle_branch, true_func, false_func)

    (handle_loop, func0, func1, func2, ...)

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
'''


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


# This primitive permits us to create a sort of "constant" in the dictionary.

def enstacken((stack, dictionary), stack_us):
    '''
    Push the items in the body onto the stack.
    '''
    stack = push(stack, *stack_us[1:])
    return stack, dictionary


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


'''
Library of Words
=================================

'''


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


'''
World
=================================

This module defines two classes: Serializer and World. Serializer deals
with saving history protocols to a pickle file and World deals with
interacting with an interpreter in a loop.

This module also defines a subclass of World called HistoryListWorld that
tracks history in a list object, and a couple of very basic views.

Starting with an initial interpreter (comprised of a stack of nominal
data and a dictionary of commands and possibly named state "variables")
the user issues a command to the interpreter which then results in a new
state (which can be the same as the initial state.)

The interpreter is embedded in a frame (a World or subclass) which
provides view and history and serialization controls.

These frame "meta" controls are several:

Change the view function.
^^^^^^^^^^^^^^^^^^^^^^^^^

View functions take a state (interpreter, stack and dictionary) and
render it somehow for the user.

Implied but not necessary are means for direct manipulation of views
to send commands to the interpreter.  It may well turn out that tight
feedback loops between views and modeled states will require a
relaxation of the strict functional style I'm striving for here.

In any event, views take a state and render it.

Views may render as text in a terminal or GUI text widget, "direct"
graphics via Pygame, etc., GUI systems such as Tkinter or wxPython,
document formats like Postscript or PDF, graphs using matplotlib or
other libraries in formats such as PNG or SVG, or web UIs using HTML,
CSS, Javascript, and perhaps even ActionScript (Flash).

Examine history and change to previous states.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The chief advantage of storing all history is in the ease of going
back and trying something new from a previous point in time.

This requires some means of indexing and displaying the states in
your history and your path through them so you can decide when to go
back to, and a way to actually go back and set your current state to
a previous state and add the transition to the history.

This seems to require another kind of view that can display not just
one state time-slice of your history, but also the tree-like path
from state to state you took.

(There is an infinite regression here: do you keep the history of the
changing of the history?  What about the history of the keeping of
that history, do you keep that too?  And that keeping's history?
Etc...  In practice we are likely to make do with only one level of
history.)

In addition to simply stepping back and forth in time, we will also
want to "pull" data from different history states, possibly in
multiple stored pickle files, and combine them in a new synthesized
states.  We can build new interpreters with the data and commands we
need to perform tasks and achieve our goals.

As yet, this script provides only indirect means to manipulate and view
history.  You can use a HistoryListWorld and manipulate its history
attribute, which is a list containing all the states of the system in
order starting with the initial state.

Manipulate external save files.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The histories must be stored in python pickle files in some external
media (i.e. a disk drive or memory stick) and there are issues of
selecting and loading histories and managing the relations between
them.

Currently this script provides no direct means to do any of this.

You can pass a file name or open file object to the World as its
save_file argument and that will be used to save the pickle data as
you use the World object, but other than that you're on your own.
'''


def view0(I):
    '''Print the stack to stdout with python's default formatting.'''
    print repr(I[0])
    print


def view1(I):
    '''Print the stack to stdout using the pprint module.'''
    pprint.pprint(I[0])
    print


def nullView(I):
    '''"Do nothing" view.'''
    pass


# An initial interpreter to use for spawning worlds.  It has an empty
# stack and whatever commands are defined by default in the library
# module.
ROOT = (), fill_tree((), words)


class World(object):
    '''
    Manage an interpreter, a view function, and serialization to a file
    or file-like object.

    This object takes a view function (any callable that accepts an
    interpreter) and optionally an initial interpreter and a save file.
    It creates a Serializer object to save commands and results, and it
    provides a step() method that accepts a command (list of strings) and
    runs it on the interpreter then saves it and calls the view function.

    '''

    def __init__(self, view=nullView, initial=None, save_file=None):
        '''
        Create a World object with the given view function.

        Keyword arguments:

        initial -- An interpreter to use as the initial state of the
            system.  It defaults to ROOT.

        save_file -- A file or file-like object open for writing, or a
            string file name which is then opened for writing. If not
            given a StringIO object is used.

        '''
        if initial is None:
            initial = ROOT

        if save_file is None:
            save_file = StringIO.StringIO()

        elif isinstance(save_file, basestring):
            save_file = open(save_file, 'w')

        # If save_file isn't None or a string or unicode object then we
        # assume it's a file-like object suitable for the Pickler.
        assert hasattr(save_file, 'write'), repr(save_file)

        self.serializer = Serializer(initial, save_file)
        self._view = view
        self.setCurrentState(initial)

    def view(self, state):
        self._view(state)

    def step(self, command):
        '''
        Run one command, a list of strings, on the interpreter then save
        the command and resulting new interpreter to the serialized
        stream and call the view function on the new interpreter.
        '''
        I = self.getCurrentState()

        # Run the command.
        I = interpret(I, command)

        # Record the resultant state.
        self.setCurrentState(I)

        # Save the command and its resultant state in the serializer. The
        # history list in the HistoryListWorld subclass serves as a sort
        # of cache on the contents of the serializer pickle stream.  (The
        # Pickler object's memo dict essentially keeps this cache for us
        # but I don't want to introduce a bunch of tight coupling with
        # the pickle medule, despite the fact that it is likely to be
        # pretty stable.)
        self.serializer.post(command, I)

    def changeView(self, view):
        '''
        Swap the current view function for the one passed, return the old
        view function.  Calls the new view.
        '''
        view, self._view = self._view, view
        self.view(self.getCurrentState())
        return view

    def setCurrentState(self, state):
        '''
        Sets current state to the passed state.  This method exists
        mostly to be overridden in subclasses.
        '''
        self.current = state
        # Render the view.
        self.view(state)

    def getCurrentState(self):
        '''
        Return the current state.  This method exists mostly to be
        overridden in subclasses.
        '''
        return self.current


class HistoryListWorld(World):
    '''
    A subclass of World that overrides the setCurrentState() and
    getCurrentState() methods to record states in a history list.
    '''

    def setCurrentState(self, state):
        '''
        Set current state to passed in state. Overrides super-class.
        '''
        try:
            history = self.history
        except AttributeError:
            history = self.history = []
        history.append(state)
        self.view(state)

    def getCurrentState(self):
        '''
        Return the current state. Overrides super-class.
        '''
        # Current state is just the most recent history.
        return self.history[-1]


class Serializer:
    '''
    Combines a Pickler and a file or file-like object to track a linear
    protocol of state -> command -> resultant-state history.

    You instantiate it with an initial state (i.e. your "root" stack and
    dictionary) and a file(-like object) to save to then you call post()
    repeatedly with the next command and the resultant stack and
    dictionary.

    The Pickler keeps a memo dict of the objects it has seen and pickled
    already and when it sees them again it serializes a reference to them
    rather than the whole object, automatically providing a sort of
    compression for the persistant datastructures we're storing in the
    pickle stream.

    You can open the pickle file and call load() repeatedly to get a
    sequence of state, command, state, ...  There will always be an odd
    number of stored data: the initial state followed by zero or more
    pairs of command and result state.
    '''

    def __init__(self, initial_state, stream):
        self.stream = stream
        self._setup_flushers(stream)
        self.pickler = pickle.Pickler(stream)
        self.pickler.dump(initial_state)
        self.flush()

    def post(self, command, resultant_state):
        '''
        Serialize command and resultant_state to the pickle stream. Each
        is saved separately so you can load a command from the stream and
        examine it without loading its resultant state.
        '''
        self.pickler.dump(command)
        self.pickler.dump(resultant_state)
        self.flush()

    def flush(self):
        for f in self._flushers:
            f()

    def _setup_flushers(self, stream):
        self._flushers = []
        if hasattr(stream, 'flush'):
            self._flushers.append(stream.flush)
        if hasattr(stream, 'fileno'):
            self._flushers.append(lambda n=stream.fileno(): os.fsync(n))


# This is a proof-of-concept frame for interacting with
# a xerblin interpreter.
if __name__ == "__main__":

    # Create a world with the basic view function.
    w = HistoryListWorld(view0)

    # For convenience print out the commands in the dictionary at
    # startup.
    dictionary = w.getCurrentState()[1]
    print ' '.join(name for name, value in items(dictionary))
    print

    # Drop into an event loop.
    while True:
        
        try:
            # Get a command and split it up.
            command = raw_input('> ').split()
        
        except EOFError:
            # User is done, quit.
            break
        
        # Run the command, the World object handles all the details for
        # us.
        w.step(command)

##
## Example run:
##
## ()
##
## NewBranchWord NewLoopWord NewSeqWord add drop dup inscribe listwords
## lookup mul over pick pickle rebalance sub swap tuck unpickle view
##
## > 23 18
## (18, (23, ()))
##
## > over
## (23, (18, (23, ())))
##
## > over
## (18, (23, (18, (23, ()))))
##
## > swap
## (23, (18, (18, (23, ()))))
##
## > sub
## (-5, (18, (23, ())))
##
## > drop
## (18, (23, ()))
##
## > over over sub
## (5, (18, (23, ())))
##
## > drop drop drop
## ()
##
## > 
##
##
