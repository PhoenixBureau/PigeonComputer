% When the program asm is expressed in Prolog we can easily specify
% transformations to apply.  Something like this...


% - can't die after set switch
t, [set_switch] --> [set_switch, or_die], t.

% - collapse pairs of labels
t, [label(L)] --> [label(L), label(L)], t.

t,          [A] --> [A], t.
t               --> [].

% - eliminate pointless goto-here's
% This one has to be done after ground terms are assigned to
% label vars to prevent spurious matches.
t2, [] --> [if_not_switch_goto(L), label(L)], t2.

