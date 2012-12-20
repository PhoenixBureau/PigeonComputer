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
