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
from Tkinter import Tk, END
from pigeon.xerblin.btree import items


def main(
  title,
  shell,
  world,
  text=None,
  text_file_name=None,
  initial=None,
  save_file=None,
  commit_thing=None,
  ):

  tk = Tk()
  tk.title(title)
  t = shell(tk, text_file_name)
  w = world(
    t.text,
    t.view,
    initial=initial,
    save_file=save_file,
    commit_thing=commit_thing,
    )

  if text is None:
    stack, dictionary = w.getCurrentState()
    words = sorted(name for name, value in items(dictionary))
    text = 'Words: ' + ' '.join(words) + '\n'

  t.text.insert(END, text)

  tk.mainloop()
