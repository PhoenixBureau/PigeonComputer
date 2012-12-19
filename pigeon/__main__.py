from Tkinter import Tk, END
from pigeon.xerblin.btree import items
from pigeon.xerblin.world import World
from pigeon.xerblin.tkworld import TkShell, TextViewerWorldMixin


class TextViewerWorld(TextViewerWorldMixin, World, object):
    pass


tk = Tk()
tk.title('Xerblin TkShell')
t = TkShell(tk)
w = TextViewerWorld(t.text, t.view)

stack, dictionary = w.getCurrentState()
words = sorted(name for name, value in items(dictionary))
t.text.insert(END, 'Words: ' + ' '.join(words) + '\n')

tk.mainloop()
