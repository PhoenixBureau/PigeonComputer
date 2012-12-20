from os.path import expanduser, exists, join
from argparse import ArgumentParser
from pickle import Unpickler
import logging, sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# First parse command line args if any.
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

# Execute the config file.
config_file = join(args.roost, args.config)

if not exists(config_file):
  config_file = config_file + '.py'

if exists(config_file):
  execfile(config_file)


# Open and read the last saved state.
text_file_name = join(args.roost, 'log')
text = open(text_file_name).read()

state_file_name = join(args.roost, 'system.pickle')
up = Unpickler(open(state_file_name))
# Pull out all the sequentially saved state, command, state, ... data.
# This loop will break after the last saved state is loaded leaving
# the last saved state in the 'state' variable
while True:
  try:
    state = up.load()
  except EOFError:
    break


# Create a commit_thing to let us save our state to the git repo after
# changes.
from pigeon.xerblin.gitstore import make_commit_thing
commit_thing = make_commit_thing(args.roost, ['log', 'system.pickle'])


# Now that the config_file has had a chance to do its thing, import the
# system and run.
from pigeon.xerblin.tkworld import TkShell, TextViewerWorld
from pigeon import main

main(
  'Pigeon Computer',
  TkShell,
  TextViewerWorld,
  text=text,
  text_file_name=text_file_name,
  initial=state,
  save_file=state_file_name, # This will cause the state_file to immediately
                             # be overwritten with the (pickled) state, thus
                             # clearing previous stored states in the saved
                             # state_file and re-starting it rooted at the
                             # current (last-saved) state.
  commit_thing=commit_thing,
  )
