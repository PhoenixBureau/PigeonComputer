#!/usr/bin/env python
"""
    Copyright (C) 2004-8 Simon Forman

    This file is part of Xerblin.

    Xerblin is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from Tkinter import (
    Text,
    Toplevel,
    TclError,
    END,
    INSERT,
    SEL,
    DISABLED,
    NORMAL,
    )
import re
from traceback import format_exc
from xerblin.messaging import ModelMixin, Viewer


#Do-nothing event handler.
nothing = lambda event : None


class mousebindingsmixin:
    """TextViewerWidget mixin class to provide mouse bindings."""

    def __init__(self):

        #Remember our mouse button state
        self.B1_DOWN = False
        self.B2_DOWN = False
        self.B3_DOWN = False

        #Remember our pending action.
        self.dothis = nothing

        #We'll need to remember whether or not we've been moving B2.
        self.beenMovingB2 = False

        #Unbind the events we're interested in.
        for sequence in (
            "<Button-1>", "<B1-Motion>", "<ButtonRelease-1>",
            "<Button-2>", "<B2-Motion>", "<ButtonRelease-2>",
            "<Button-3>", "<B3-Motion>", "<ButtonRelease-3>",
            "<B1-Leave>", "<B2-Leave>", "<B3-Leave>", "<Any-Leave>", "<Leave>"
            ):
            self.unbind(sequence)
            self.unbind_all(sequence)

        self.event_delete('<<PasteSelection>>') #I forgot what this was for! :-P  D'oh!

        #Bind our event handlers to their events.
        self.bind("<Button-1>", self.B1d)
        self.bind("<B1-Motion>", self.B1m)
        self.bind("<ButtonRelease-1>", self.B1r)

        self.bind("<Button-2>", self.B2d)
        self.bind("<B2-Motion>", self.B2m)
        self.bind("<ButtonRelease-2>", self.B2r)

        self.bind("<Button-3>", self.B3d)
        self.bind("<B3-Motion>", self.B3m)
        self.bind("<ButtonRelease-3>", self.B3r)

        self.bind("<Any-Leave>", self.leave)

    def B1d(self, event):
        '''button one pressed'''
        self.B1_DOWN = True

        if self.B2_DOWN:

            self.unset_command()

            if self.B3_DOWN :
                self.dothis = self.cancel

            else:
                #copy TOS to the mouse (instead of system selection.)
                self.dothis = self.copyto #middle-left-interclick

        elif self.B3_DOWN :
            self.unset_command()
            self.dothis = self.opendoc #right-left-interclick

        else:
            ##button 1 down, set insertion and begin selection.
            ##Actually, do nothing. Tk Text widget defaults take care of it.
            self.dothis = nothing
            return

        #Prevent further event handling by returning "break".
        return "break"

    def B2d(self, event):
        '''button two pressed'''
        self.B2_DOWN = 1

        if self.B1_DOWN :

            if self.B3_DOWN :
                self.dothis = self.cancel

            else:
                #left-middle-interclick - cut selection to stack
                self.dothis = self.cut

        elif self.B3_DOWN :
            self.unset_command()
            self.dothis = self.lookup #right-middle-interclick - lookup

        else:
            #middle-click - paste X selection to mouse pointer
            self.set_insertion_point(event)
            self.dothis = self.paste_X_selection_to_mouse_pointer
            return

        return "break"

    def B3d(self, event):
        '''button three pressed'''
        self.B3_DOWN = 1

        if self.B1_DOWN :

            if self.B2_DOWN :
                self.dothis = self.cancel

            else:
                #left-right-interclick - copy selection to stack
                self.dothis = self.copyfrom

        elif self.B2_DOWN :
            #middle-right-interclick - Pop/Cut from TOS to insertion cursor
            self.unset_command()
            self.dothis = self.pastecut

        else:
            #right-click
            self.CommandFirstDown(event)

        return "break"

    def B1m(self, event):
        '''button one moved'''
        if self.B2_DOWN or self.B3_DOWN:
            return "break"

    def B2m(self, event):
        '''button two moved'''
        if self.dothis == self.paste_X_selection_to_mouse_pointer and \
           not (self.B1_DOWN or self.B3_DOWN):

            self.beenMovingB2 = True
            return

        return "break"

    def B3m(self, event):
        '''button three moved'''
        if self.dothis == self.do_command and \
           not (self.B1_DOWN or self.B2_DOWN):

            self.update_command_word(event)

        return "break"

    def B1r(self, event):
        '''button one released'''
        self.B1_DOWN = False

        if not (self.B2_DOWN or self.B3_DOWN):
            self.dothis(event)

        return "break"

    def B2r(self, event):
        '''button two released'''
        self.B2_DOWN = False

        if not (self.B1_DOWN or self.B3_DOWN or self.beenMovingB2):
            self.dothis(event)

        self.beenMovingB2 = False

        return "break"

    def B3r(self, event):
        '''button three released'''
        self.B3_DOWN = False

        if not (self.B1_DOWN or self.B2_DOWN) :
            self.dothis(event)

        return "break"

    def InsertFirstDown(self, event):
        self.focus()
        self.dothis = nothing
        self.set_insertion_point(event)

    def CommandFirstDown(self, event):
        self.dothis = self.do_command
        self.update_command_word(event)


class TextViewerWidget(Text, mousebindingsmixin):
    """
    This class is a Tkinter Text with special mousebindings to make
    it act as a Xerblin Text Viewer.
    """

    #This is a regular expression for finding commands in the text.
    command_re = re.compile(r'[-a-zA-Z0-9_\\~/.:!@#$%&*?=+]+')

    #These are the config tags for command text when it's highlighted.
    command_tags = dict(
        underline = 1,
        bgstipple = "gray50",
        borderwidth = "1",
        foreground = "orange"
    )

    def __init__(self, master=None,  **kw):

        #Get our Interpreter, and remove the arg to get it out of Tkinter's way.
        self.interpreter = kw.pop('interpreter')
        self.model = kw.pop('model', None)

##        self.interpreter.windows.append(self)

        #Turn on undo, but don't override a passed-in setting.
        kw.setdefault('undo', True)

##        kw.setdefault('bg', 'white')
        kw.setdefault('wrap', 'word')
        kw.setdefault('font', 'arial 12')

        #Create ourselves as a Tkinter Text
        Text.__init__(self, master, **kw)

        #Initialize our mouse mixin.
        mousebindingsmixin.__init__(self)

        #Add tag config for command highlighting.
        self.tag_config('command', **self.command_tags)

        #Create us a command instance variable
        self.command = ''

        #I want to ensure that these keyboard shortcuts work.
        for s in ('<Control-v>', '<Control-V>', '<Shift-Insert>'):
            self.bind(s, self._paste)

        self.tk.call(self._w, 'edit', 'modified', 0)
        self.bind('<<Modified>>', self._beenModified)
        self._resetting_modified_flag = False

##        T.protocol("WM_DELETE_WINDOW", self.onclose(T))

    def _beenModified(self, event):
        if self._resetting_modified_flag:
            return
        self._clearModifiedFlag()
        self.save()

    def _clearModifiedFlag(self):
        self._resetting_modified_flag = True
        try:
            self.tk.call(self._w, 'edit', 'modified', 0)
        finally:
            self._resetting_modified_flag = False

    _saveDelay = 450

    def save(self):
        '''
        Call _saveFunc() after a certain amount of idle time.

        Called by _beenModified().
        '''
        self._cancelSave()
        self._saveAfter(self._saveDelay)

    def _saveFunc(self):
        self._save = None

        data = self.get('0.0', END)[:-1]
        self['state'] = DISABLED
        try:
            self.model.value = data
        finally:
            self['state'] = NORMAL

##        tags = self._saveTags()
##        chunks = self.DUMP()
##        print chunks

    def _saveAfter(self, delay):
        '''
        Trigger a cancel-able call to _saveFunc() after delay milliseconds.
        '''
        self._save = self.after(delay, self._saveFunc)

    def _cancelSave(self):
        try:
            save = self._save
        except AttributeError:
            pass
        else:
            if save:
                self.after_cancel(save)
                save = None

    def findCommandInLine(self, line, index):
        '''findCommandInLine(line, index) => command, begin, end
        Return the command at index in line and its begin and end indices.'''

        #Iterate through the possible commands in the line...
        for match in self.command_re.finditer(line):

            #Pull out the indices of the possible command.
            b, e = match.span()

            #If the indices bracket the index return the result.
            if b <= index <= e:
                return match.group(), b, e

    def paste_X_selection_to_mouse_pointer(self, event):
        '''paste the X selection to the mouse pointer.'''

        #Use the Tkinter method selection_get() to try to get the X selection.
        try:
            text = self.selection_get()

        #TclError gets raised if no current selection.
        except TclError:

            #So just carry on, there's nothing to do.
            return 'break'

        #We got a selection. Put it on the stack.
        self.interpreter.stack.insert(0, text)

        #Send ourselves a copyto event.
        self.copyto(event)

        #And simulate the cut by popping the text off the stack.
        self.interpreter.stack.pop(0)

    def update_command_word(self, event):
        '''Highlight the command under the mouse.'''

        #Get rid of any old command highlighting.
        self.unset_command()

        #Get the index of the mouse.
        index = '@%d,%d' % (event.x, event.y)

        #Find coordinates for the line under the mouse.
        linestart = self.index(index + 'linestart')
        lineend   = self.index(index + 'lineend')

        #Get the entire line under the mouse.
        line = self.get(linestart, lineend)

        #Parse out the row and offset of the mouse
        row, offset = self._get_index(index)

        #If the mouse is off the end of the line or on a space..
        if offset >= len(line) or line[offset].isspace():

            #There's no command, we're done.
            self.command = ''
            return

        #Get the command at the offset in the line.
        cmd = self.findCommandInLine(line, offset)

        if cmd and (
            cmd[0] in self.interpreter.dictionary or isNumerical(cmd[0])):

            #Set self's command variable and extract the indices of it.
            self.command, b, e = cmd

            #Get the indices relative to the Text.
            cmdstart = self.index('%d.%d' % (row, b))
            cmdend   = self.index('%d.%d' % (row, e))

            #Add the command highlighting tags to the command text.
            self.tag_add('command', cmdstart, cmdend)

        #If there was no command, clear our command variable.
        else:
            self.command = ''

    def do_command(self, event):
        '''Do the currently highlighted command.'''

        #Remove any old highlighting.
        self.unset_command()

        #If there is a current command..
        if self.command:

            #Interpret the current command.
            try:
                self.interpreter.interpret(self.command)
            except SystemExit:
                raise
            except:
                data = format_exc().rstrip()
                self.popupTB(data)

    def unset_command(self):
        '''Remove any command highlighting.'''
        self.tag_remove('command', 1.0, END)

    def set_insertion_point(self, event):
        '''Set the insertion cursor to the current mouse location.'''
        self.focus()
        self.mark_set(INSERT, '@%d,%d' % (event.x, event.y))

    def cut(self, event):
        '''Cut selection to stack.'''

        #Get the indices of the current selection if any.
        select_indices = self.tag_ranges(SEL)

        #If there is a current selection..
        if select_indices:

            #Get the text of it.
            s = self.get(select_indices[0], select_indices[1])

            #Append the text to our interpreter's stack.
            self.interpreter.stack.insert(0, s)

            #Let the pre-existing machinery take care of cutting the selection.
            self.event_generate("<<Cut>>")

    def copyto(self, event):
        '''Actually "paste" from TOS'''

        #If for some reason there's nothing on the stack, return.
        if not self.interpreter.stack:
            return

        #Otherwise, get the TOS item.
        s = self.interpreter.stack[0]

        #Make sure it's a string.
        if not isinstance(s, basestring):
            s = str(s)

        #When pasting from the mouse we have to remove the current selection
        #to prevent destroying it by the paste operation.

        #Find out if there's a current selection.
        select_indices = self.tag_ranges(SEL)

        #If there's a selection.
        if select_indices:

            #Remember that we have to reset it after pasting.
            reset_selection = True

            #Set two marks to remember the selection.
            self.mark_set('_sel_start', select_indices[0])
            self.mark_set('_sel_end', select_indices[1])

            #Remove the selection.
            self.tag_remove(SEL, 1.0, END)

        #If there's no selection we don't have to reset it
        else:
            reset_selection = False

        #Insert the TOS string.
        self.insert(INSERT, s)

        #If we have to reset the selection...
        if reset_selection:

            #Put the SEL tag back.
            self.tag_add(SEL, '_sel_start', '_sel_end')

            #Get rid of the marks we set.
            self.mark_unset('_sel_start')
            self.mark_unset('_sel_end')

        #Key pasting should still work fine, allowing one to select a piece
        #of text and paste to it, replacing the selection.

    def copyfrom(self, event):
        '''copy from selection to stack and system clipboard.'''

        #Get the selection.
        select_indices = self.tag_ranges(SEL)

        #If there is a selection..
        if select_indices:

            #Get the text of the selection.
            s = self.get(select_indices[0], select_indices[1])

            #Remove the SEL tag from the whole Text.
            self.tag_remove(SEL, 1.0, END)

            #Put the selection text on the system clipboard.
            self.clipboard_clear()
            self.clipboard_append(s)

            #And put it on the stack.
            self.interpreter.stack.insert(0, s)

    def pastecut(self, event):
        '''Cut the TOS item to the mouse.'''

        #Paste the TOS item to the mouse.
        self.copyto(event)

        #If that worked (we're here aren't we?)..
        if self.interpreter.stack:

            #Pop the item off the stack.
            self.interpreter.stack.pop(0)

    def opendoc(self, event):
        '''OpenDoc the current command.'''

        if not self.command:
            return

        word = self.interpreter.dictionary.get(self.command)
        if word:
            # "Bunt" for now.
            print 'opendoc', word

    def lookup(self, event):
        '''Look up the current command.'''

        if not self.command:
            return
        
        word = self.interpreter.dictionary.get(self.command)
        if word:
            #Push the current command onto the stack.
            self.interpreter.stack.insert(0, word)

    def cancel(self, event):
        '''Cancel whatever we're doing.'''
        
        #Remove any old highlighting.
        self.unset_command()

        #Unset our command variable
        self.command = ''

        #Remove the SEL tag
        self.tag_remove(SEL, 1.0, END)

        #Reset the selection anchor.
        self._sel_anchor = '0.0'

        #I don't know if this helps, or even if it does anything. But what the heck.
        self.mark_unset(INSERT)

    def leave(self, event):
        '''Called when mouse leaves the Text window.'''

        #Remove any old highlighting.
        self.unset_command()

        #Unset our command variable
        self.command = ''

    def _get_index(self, index):
        '''Get the index in (int, int) form of index.'''
        return tuple(map(int, self.index(index).split('.')))

    def _paste(self, event):
        '''Paste the system selection to the current selection, replacing it.'''

        #If we're "key" pasting, we have to move the insertion point
        #to the selection so the pasted text gets inserted at the
        #location of the deleted selection.

        #Get the current selection's indices if any.
        select_indices = self.tag_ranges(SEL)

        #If the selection exists.
        if select_indices:

            #Mark the location of the current insertion cursor 
            self.mark_set('tmark', INSERT)

            #Put the insertion cursor at the selection
            self.mark_set(INSERT, select_indices[1])

        #Paste to the current selection, or if none, to the insertion cursor.
        self.event_generate("<<Paste>>")

        #If we mess with the insertion cursor above, fix it now.
        if select_indices:

            #Put the insertion cursor back where it was.
            self.mark_set(INSERT, 'tmark')

            #And get rid of our unneeded mark.
            self.mark_unset('tmark')

        #Tell Tkinter that event handling for this event is over.
        return 'break'

    def onclose(self, T):
        def f():
            # Collect strings and objects.
            self._dying = self.DUMP()

            # Destroys ThingButton children, _dying attribute prevents
            # them from appending their objects to the stack.
            T.destroy()

            if self._dying:
                self.interpreter.stack.insert(0, self._dying)
                del self._dying

##            self.interpreter.windows.remove(self)

        return f

    def popupTB(self, tb):
        top = Toplevel()
        T = TextViewerWidget(
            top,
            interpreter=self.interpreter,
            width=max(len(s) for s in tb.splitlines()) + 3,
            )

        T['background'] = 'darkgrey'
        T['foreground'] = 'darkblue'
        T.tag_config('err', foreground='yellow')

        T.insert(END, tb)
        last_line = str(int(T.index(END).split('.')[0]) - 1) + '.0'
        T.tag_add('err', last_line, END)

        top.title(T.get(last_line, END).strip())

        T.pack(expand=1, fill='both')
        T.see(END)


class TextViewer(Viewer):

    def __init__(self, model, master=None, **kw):
        Viewer.__init__(self, model)
        kw.setdefault('model', model)
        self.text = TextViewerWidget(master, **kw)
        self.text.pack(expand=True, fill='both')
        self.update()
        self.text.update_idletasks()
        ModelMixin.root.addChild(self)

    def __getstate__(self):
        T = self.text
        master = T.winfo_toplevel()
        kw = dict((key, T[key]) for key in T.keys())
        kw['interpreter'] = T.interpreter
        model = self.model
        return model, master, kw

    def __setstate__(self, state):
        model, master, kw = state
        self.__init__(model, master, **kw)

    def insert(self, *args):
        self.text.insert(*args)

    def handle(self, message):
        if not self._checkMessage(message):
            return False

        if message.model is self.model or self._dispatch(message):
            self.update()
            return True

        return False

    def update(self):
        self.text.delete('0.0', END)
        self.text.insert('0.0', self.model.value)
        self.text._cancelSave()
        self.text._clearModifiedFlag()
        

def isNumerical(s):
    try:
        float(s)
    except ValueError:
        return False
    return True
