#!/usr/bin/env python
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
A simple Tkinter GUI.
'''
from Tkinter import Tk, Listbox, N, END, Entry, LEFT, BOTH, Y
from pigeon.xerblin.btree import items
from pigeon.xerblin.stack import iterStack
from pigeon.xerblin.TextViewer import TextViewerWidget, TextViewerWorldMixin
from pigeon.xerblin.world import World


class TextViewerWorld(TextViewerWorldMixin, World, object):
    pass


class TkShell:

    def __init__(self, root, text_file_name):
        self._create_widgets(root, text_file_name)
        self.words = []

    def view(self, (stack, dictionary)):
        self._update_listbox(self.stack_view, iterStack(stack))

    def _update_listbox(self, listbox, contents):
        contents = list(
            '%s: %r' % (getattr(type(it), '__name__', type(it)), it)
            for it in contents
            )
        listbox.delete(0, END)
        listbox.insert(0, *contents)

    def _create_widgets(self, root, text_file_name):
        self.stack_view = Listbox(root, width=64)
        self.stack_view.pack(side=LEFT, expand=True, fill=BOTH)
        self.text = TextViewerWidget(root, filename=text_file_name)
        self.text.pack(side=LEFT, expand=True, fill=BOTH)


if __name__ == "__main__":
    tk = Tk()
    tk.title('Xerblin TkShell')

    t = TkShell(tk)
    w = TextViewerWorld(t.text, t.view)

    dictionary = w.getCurrentState()[1]
    words = sorted(name for name, value in items(dictionary))
    t.text.insert(END, 'Words: ' + ' '.join(words) + '\n')

    tk.mainloop()
