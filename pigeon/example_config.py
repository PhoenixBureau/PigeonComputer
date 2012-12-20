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
