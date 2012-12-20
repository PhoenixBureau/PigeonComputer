from Tkinter import Tk, END
from pigeon.xerblin.btree import items


def main(title, shell, world, text=None, initial=None, save_file=None):
  tk = Tk()
  tk.title(title)
  t = shell(tk)
  w = world(t.text, t.view, initial=initial, save_file=save_file)

  if text is None:
    stack, dictionary = w.getCurrentState()
    words = sorted(name for name, value in items(dictionary))
    text = 'Words: ' + ' '.join(words) + '\n'

  t.text.insert(END, text)

  tk.mainloop()
