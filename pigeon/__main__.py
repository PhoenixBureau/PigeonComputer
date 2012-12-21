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
  help=('Use this directory as home for the Pigeon system. (default: %(default)s).\n'
        '(I apologize for the terrible pun.)'),
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
with open(state_file_name) as f:
  up = Unpickler(f)
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
