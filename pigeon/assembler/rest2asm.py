#!/usr/bin/env python
'''
This is a simple script to read a reStructuredText file and extract all
the code definitions (the "literal-block" content) and print them out.

Use this to transform e.g. docs/pigeon_firmware.rst to asm.py like so::

    ./rest2asm.py ../docs/pigeon_firmware.rst > asm.py

'''
# There's probably a way to get the content directly from the docutils
# stuff without going through HTML output and BeautifulSoup parsing but I
# don't have the spare time to figure it out at the moment.  (And this
# works fine.)
import sys
from BeautifulSoup import BeautifulStoneSoup
from docutils.core import publish_parts


if len(sys.argv) > 1:
  data = open(sys.argv[-1]).read()
else:
  data = sys.stdin.read()


parts = publish_parts(data, writer_name='html')
html_body = parts['html_body']
soup = BeautifulStoneSoup(
  html_body,
  convertEntities=BeautifulStoneSoup.ALL_ENTITIES,
  )


for p in soup.findAll('pre', { "class" : "literal-block" }):
  for c in p.contents:
    sys.stdout.write(c)

