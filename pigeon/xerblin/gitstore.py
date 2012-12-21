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
import pickle, logging, sys
from os.path import exists, join
from dulwich.repo import Repo, NotGitRepository
from pigeon.xerblin.btree import items


def make_commit_thing(path, files):
  log = logging.getLogger('COMMIT')
  try:
    repo = Repo(path)
  except NotGitRepository:
    log.critical("%r isn't a repository!", path)
    raise ValueError("%r isn't a repository!" % (path,))

  # Note that we bind the args as defaults rather than via a closure so
  # you can override them later if you want.
  def commit(message, files=files, repo=repo, log=log):
    repo.stage(files)
    commit_sha = repo.do_commit(message)
    log.info('commit %s %s', commit_sha, message[:100])

  return commit


def list_words(dictionary):
  words = sorted(name for name, value in items(dictionary))
  return 'Words: ' + '   '.join(words) + '\n'


def initialize_repo(path, state, text, create_default_config=True):
  log = logging.getLogger('INIT_REPO')
  if not exists(path):
    log.critical("%r doesn't exist!", path)
    raise ValueError("%r doesn't exist!" % (path,))

  try:
    Repo(path)
  except NotGitRepository:
    # Good! That's what we expect.
    repo = Repo.init(path)
    log.info('%r created.', repo)
  else:
    # No good! We are an initialize function, nothing else.
    log.critical('Repository already exists at %r', path)
    raise ValueError('Repository already exists at %r' % (path,))

  text_file_name = join(path, 'log')
  open(text_file_name, 'w').write(text)
  log.info('%s written.', text_file_name)

  system_pickle_file_name = join(path, 'system.pickle')
  pickle.dump(state, open(system_pickle_file_name, 'wb'))
  log.info('%s written.', system_pickle_file_name)

  files = ['log', 'system.pickle']

  if create_default_config:
    config_file_name = join(path, 'config.py')
    open(config_file_name, 'w').write('''\
from operator import attrgetter
import pigeon.xerblin.TextViewer


# Add some text widget keybindings.
pigeon.xerblin.TextViewer.text_bindings.update({
  '<F4>': attrgetter('copyfrom'), # Copy from selection to stack and system clipboard.
  '<Shift-F4>': attrgetter('cut'), # Cut selection to stack and system clipboard.
  '<F6>': attrgetter('cut'), # ditto.
  '<F5>': attrgetter('copyto'), # Paste from stack to cursor (leave stack undisturbed.)
  '<Shift-F5>': attrgetter('pastecut'), # Paste from stack to cursor and pop stack.
  '<F7>': attrgetter('pastecut'), # ditto.
  })
''')
    log.info('%s written.', config_file_name)
    files.append('config.py')

  repo.stage(files)
  staged = list(repo.open_index())
  log.info('Files staged: ' + ', '.join(['%s'] * len(staged)), *staged)
  commit = repo.do_commit('Initial commit.')
  log.info('Initial commit done. %s', commit)


if __name__ == "__main__":
  from pigeon.xerblin.world import ROOT
  initialize_repo(
    '/home/sforman/.pigeon',
    ROOT,
    list_words(ROOT[1]),
    False,
    )
