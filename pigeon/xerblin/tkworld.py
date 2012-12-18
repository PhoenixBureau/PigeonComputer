#!/usr/bin/env python
'''
A simple Tkinter GUI.
'''
from shlex import split
from Tkinter import Tk, Listbox, N, END, Entry, LEFT, BOTH, Y
from pigeon.xerblin.btree import items
from pigeon.xerblin.stack import iterStack
from pigeon.xerblin.TextViewer import TextViewerWidget, TextViewerWorldMixin


class TkShell:

    def __init__(self, root):
        self._create_widgets(root)
        self.words = []

    def view(self, (stack, dictionary)):
        self._update_listbox(self.stack_view, iterStack(stack))

    def _update_listbox(self, listbox, contents):
        contents = list(contents)
        listbox.delete(0, END)
        listbox.insert(0, *contents)

    def _create_widgets(self, root):
        self.stack_view = Listbox(root, width=64)
        self.stack_view.pack(side=LEFT, expand=True, fill=BOTH)
        self.text = TextViewerWidget(root)
        self.text.pack(side=LEFT, expand=True, fill=BOTH)


if __name__ == "__main__":
    from pigeon.xerblin.world import HistoryListWorld

    class World(TextViewerWorldMixin, HistoryListWorld, object):
        pass

    tk = Tk()
    tk.title('Xerblin TkShell')

    t = TkShell(tk)
    w = World(t.text, t.view)

    dictionary = w.getCurrentState()[1]
    words = sorted(name for name, value in items(dictionary))
    t.text.insert(END, 'Words: ' + ' '.join(words) + '\n')

    tk.mainloop()
