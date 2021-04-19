.SUFFIXES :
DIFF = diff --report-identical-files

all: newlang5.asm

# newlang5.asm uses the new op codes.
# It is a metacompiler using the new VM.
newlang5.out: metaii.5.py newlang5.asm newlang5.newlang5
	./metaii.5.py -p newlang5.asm newlang5.newlang5 > newlang5.out
	$(DIFF) newlang5.asm newlang5.out

# The Python compiler-to-asm regenerates the original asm.
# Note the '-w' switch to tell diff to ignore differences in whitespace
newlang5.asm: newlang5asm.py newlang5.newlang5 metaii_base.py
	python3 newlang5asm.py < newlang5.newlang5 > newlang5.asm
	$(DIFF) -w newlang5.out newlang5.asm


