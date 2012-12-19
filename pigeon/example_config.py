from operator import attrgetter
import pigeon.xerblin.gitstorage
import pigeon.xerblin.TextViewer


# Modify the default Git settings.
pigeon.xerblin.gitstorage.GIT_ROOT = args.roost
pigeon.xerblin.gitstorage.AUTHOR = 'Simon Forman <simon@pigeoncomputer.org>'
pigeon.xerblin.gitstorage.TZ = '-0800'


# Add some text widget keybindings.
pigeon.xerblin.TextViewer.text_bindings.update({
  '<F4>': attrgetter('copyfrom'), # Copy from selection to stack and system clipboard.
  '<Shift-F4>': attrgetter('cut'), # Cut selection to stack and system clipboard.
  '<F6>': attrgetter('cut'), # ditto.
  '<F5>': attrgetter('copyto'), # Paste from stack to cursor (leave stack undisturbed.)
  '<Shift-F5>': attrgetter('pastecut'), # Paste from stack to cursor and pop stack.
  '<F7>': attrgetter('pastecut'), # ditto.
  })
