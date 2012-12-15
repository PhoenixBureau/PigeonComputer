#!/usr/bin/env python
'''
A simple Tkinter GUI.
'''
from shlex import split
from Tkinter import Tk, Listbox, N, END, Entry, N, W, E, S
from xerblin.btree import items
from xerblin.stack import iterStack
from xerblin.world import HistoryListWorld


class TkShell:

    def __init__(self, root):
        self._create_widgets(root)

    def set_world(self, world):
        self.world = world
        world.changeView(self.view)

    def view(self, (stack, dictionary)):
        self._update_stack(stack)
        self._update_dictionary(dictionary)

    def _update_stack(self, stack):
        self._update_listbox(self.stack_view, iterStack(stack))

    def _update_dictionary(self, dictionary):
        words = (name for name, value in items(dictionary))
        self._update_listbox(self.dictionary_view, words)

    def _update_listbox(self, listbox, contents):
        contents = list(contents)
        listbox.delete(0, END)
        listbox.insert(0, *contents)
        listbox['height'] = max(10, len(contents) + 1)

    def _create_widgets(self, root):
        self.stack_view = Listbox(root)
        self.stack_view.grid(sticky=N+W+E+S)
        self.dictionary_view = Listbox(root)
        self.dictionary_view.grid(row=0, column=1, sticky=N+W+E+S)
        self.dictionary_view.bind("<Button-1>", self.command)

        self.e = Entry(root)
        self.e.grid(row=1, column=0, columnspan=2, sticky=N+W+E+S)
        self.e.bind("<Return>", self.run_entry_command)

    def run_entry_command(self, event):
        command = self.e.get()
        if not command:
            return
        command = list(_split_command(command))
        self.world.step(command)
        self.e.delete(0, 'end')

    def command(self, event):
        # Calculate the relative mouse coordinates as a '@x,y' string.
        i = '@%(x)i,%(y)i' % event.__dict__
        # Look up the word under the mouse.
        i = self.dictionary_view.index(i)
        word = self.dictionary_view.get(i)
        # Execute it.
        self.world.step([word])



def _split_command(command):
    for word in split(command):
        if not word or ' ' in word:
            word = '"%s"' % word
        yield word


if __name__ == "__main__":
    tk = Tk()
    tk.title('Xerblin TkShell')

    w = HistoryListWorld()
    w.step('23 18'.split())

    t = TkShell(tk)
    t.set_world(w)

    tk.mainloop()
