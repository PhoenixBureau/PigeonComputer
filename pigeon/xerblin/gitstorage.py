import os, pickle
from time import time
from dulwich.repo import Repo, NotGitRepository
from dulwich.objects import Blob, Tree, Commit, parse_timezone


GIT_ROOT = os.path.expanduser('~/.xerblin')
AUTHOR = 'Simon Forman <forman.simon@gmail.com>'
TZ = '-0800'


def get_repo(root=None):
  if root is None:
    root = GIT_ROOT
  print 'repository at', root
  try:
    return Repo(root)
  except NotGitRepository:
    return Repo.init(root)


def create_commit(tree, message, author=None, tz=None, parents=[]):
  if author is None:
    author = AUTHOR
  if tz is None:
    tz = TZ
  c = Commit()
  c.tree = tree.id
  if parents:
    c.parents = parents
  c.author = c.committer = author
  c.commit_time = c.author_time = int(time())
  c.commit_timezone = c.author_timezone = parse_timezone(tz)[0]
  c.encoding = 'UTF-8'
  c.message = message
  return c


def add_file(tree, name, contents, mode=0100644):
  blob = Blob.from_string(contents)
  tree.add(name, mode, blob.id)
  return blob


def save_state(files, message, repo=None):
  if repo is None:
    repo = get_repo()
  print 'hoo', repo
  a = repo.object_store.add_object

  try:
    parents = [repo.refs['HEAD']]
  except KeyError:
    parents = []

  tree = Tree()
  for name, contents in files.iteritems():
    if isinstance(contents, unicode):
      contents = str(contents)
    assert isinstance(contents, str), repr(contents)
    a(add_file(tree, name, contents))
  a(tree)
  c = create_commit(tree, message, parents=parents)
  a(c)
  repo.refs['refs/heads/master'] = c.id


def retrieve_head(repo_path=None):
  repo = get_repo(repo_path)
  commit = repo.get_object(repo.head())
  tree = repo.get_object(commit.tree)
  log_contents = repo.get_object(tree['log'][1])
  system_pickle = repo.get_object(tree['system'][1])
  return str(log_contents), pickle.loads(str(system_pickle))


if __name__ == '__main__':
  import random
  save_state(
    {
      'system': 'pickle data',
      'log': 'contents of text viewer',
      },
    'This would be the auto-commit.' + str(random.random())
    )
