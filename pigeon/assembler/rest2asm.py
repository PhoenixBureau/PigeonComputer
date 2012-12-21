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

