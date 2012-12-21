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
#
# This is an example of configuration for the Pigeon User Interface.
# It's just a Python file that gets execfile()'d in the context of the
# PUI system just before loading and starting the GUI.
#
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
