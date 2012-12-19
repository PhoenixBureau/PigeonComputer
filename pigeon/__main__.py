from os.path import expanduser, exists, join
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
from pigeon.xerblin.tkworld import TkShell, TextViewerWorld
from pigeon import main
main('Pigeon Computer', TkShell, TextViewerWorld)
