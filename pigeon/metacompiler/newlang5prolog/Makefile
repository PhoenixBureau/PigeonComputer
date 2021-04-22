.SUFFIXES :
DIFF = diff --report-identical-files

all: newlang5.pl


# Let's output some Prolog code.
newlang5pl.asm: newlang5prolog.newlang5
	./metaii.5.py -p newlang5.asm newlang5prolog.newlang5 > newlang5pl.asm

newlang5.pl: newlang5prolog.newlang5 newlang5pl.asm
	./metaii.5.py -p newlang5pl.asm newlang5prolog.newlang5 > newlang5.pl

clean:
	rm -vf newlang5pl.asm newlang5.pl

