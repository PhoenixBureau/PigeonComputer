from os.path import expanduser, exists, join
from Tkinter import Tk, END
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
    '-r', '--roost',
    default=expanduser('~/.pigeon'),
    help='Use this directory as home for the Pigeon system. (default: %(default)s).',
    )
parser.add_argument(
    '-c', '--config',
    default=expanduser('config.py'),
    help='Use this config file.')
args = parser.parse_args()


config_file = join(args.roost, args.config)
if not exists(config_file):
    config_file = config_file + '.py'
if exists(config_file):
    execfile(config_file)

# Now that the config_file has had a chance to do its thing, import the
# system and run.
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
