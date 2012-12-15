#!/usr/bin/env python
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

Code Documentation
^^^^^^^^^^^^^^^^^^

'''
import pickle, pprint, StringIO
from xerblin.btree import fill_tree, items
from xerblin.library import words
from xerblin.base import interpret


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


class World:
    '''
    Manage an interpreter, a view function, and serialization to a file
    or file-like object.

    This object takes a view function (any callable that accepts an
    interpreter) and optionally an initial interpreter and a save file.
    It creates a Serializer object to save commands and results, and it
    provides a step() method that accepts a command (list of strings) and
    runs it on the interpreter then saves it and calls the view function.

    '''

    def __init__(self, view=nullView, initial=ROOT, save_file=None):
        '''
        Create a World object with the given view function.

        Keyword arguments:

        initial -- An interpreter to use as the initial state of the
            system.  It defaults to ROOT.
        
        save_file -- A file or file-like object open for writing, or a
            string file name which is then opened for writing. If not
            given a StringIO object is used and its getvalue() method is
            made available on the World object as the attribute
            "_getvalue".

        '''

        if save_file is None:
            save_file = StringIO.StringIO()
            self._getvalue = save_file.getvalue # We're gonna want this.

        elif isinstance(save_file, basestring):
            save_file = open(save_file, 'w')

        # If save_file isn't None or a string or unicode object then we
        # assume it's a file-like object suitable for the Pickler.
        assert hasattr(save_file, 'write'), repr(save_file)

        self.serializer = Serializer(initial, save_file)
        self.setCurrentState(initial)
        self.view = view
        self.view(initial)

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

        # Render the view.
        self.view(I)

    def changeView(self, view):
        '''
        Swap the current view function for the one passed, return the old
        view function.  Calls the new view.
        '''
        view, self.view = self.view, view
        self.view(self.getCurrentState())
        return view

    def setCurrentState(self, state):
        '''
        Sets current state to the passed state.  This method exists
        mostly to be overridden in subclasses.
        '''
        self.current = state

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
        self.pickler = pickle.Pickler(stream)
        self.pickler.dump(initial_state)

    def post(self, command, resultant_state):
        '''
        Serialize command and resultant_state to the pickle stream. Each
        is saved separately so you can load a command from the stream and
        examine it without loading its resultant state.
        '''
        self.pickler.dump(command)
        self.pickler.dump(resultant_state)


# This is a proof-of-concept frame for interacting with
# a xerblin interpreter.
if __name__ == "__main__":

    from xerblin.btree import items

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
