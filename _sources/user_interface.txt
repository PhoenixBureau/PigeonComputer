Pigeon User Interface
============================================

The Pigeon User Interface is a simple but powerful way to interact with
your computer.  It's a general system but I've customized it here for
experimenting and playing with the Pigeon software and hardware.

It consists of a *Text* window that displays editable text, and a *Stack*
of data items with a *Dictionary* of named functions that operate on the
Stack.  In this way it's very much like the Pigeon Firmware (TODO:
linkify) and in fact many simple commands that work on the firmware will
also work identically on the PUI (Pigeon User Interface) but the PUI is
much more powerful.

For one thing, it never forgets.

The interface stores the current state of the Stack, Dictionary and Text
after each command and whenever you change the text and pause for more
than two seconds.

You never have to save your work, and you can always go back to any
previous place in your history and access it or "restart" from it.  And,
unlike most web browsers and undo/redo functions, if you go back in
history and try a different path the previous path you took is also
still remembered, not forgotten, and can be re-accessed or re-visited at
any time.

The system never forgets, so you never have to remember to hit "save" and
you never have to worry about losing your work.  You can't anymore, the
computer protects you.




.. automodule:: pigeon.xerblin.stack

.. automodule:: pigeon.xerblin.btree

.. automodule:: pigeon.xerblin.base

.. automodule:: pigeon.xerblin.world

.. automodule:: pigeon.xerblin.library


