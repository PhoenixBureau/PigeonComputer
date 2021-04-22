.SUFFIXES :
DIFF = diff --report-identical-files
PATCH = patch --quiet -V none

all: newlang5py.py.out newlang5.asm.out


# newlang5py
# Changing the output language to Python

newlang5py.asm: metaii.5.py ../newlang5.out newlang5py.newlang5
	python3 metaii.5.py -p ../newlang5.out newlang5py.newlang5 > newlang5py.asm

newlang5py.py: metaii.5.py newlang5py.asm newlang5py.newlang5
	python3 metaii.5.py -p newlang5py.asm newlang5py.newlang5 > newlang5py.py

# This new Python script is a metacompiler.
newlang5py.py.out: newlang5py.py newlang5py.newlang5 metaii_base.py
	python3 newlang5py.py < newlang5py.newlang5 > newlang5py.py.out
	$(DIFF) newlang5py.py newlang5py.py.out

# It can compile a Python implementation of a newlang5-to-asm compiler:
newlang5asm.py: newlang5py.py ../newlang5.newlang5 metaii_base.py
	python3 newlang5py.py < ../newlang5.newlang5 > newlang5asm.py

# The Python compiler-to-asm regenerates the original asm.
# Note the '-w' switch to tell diff to ignore differences in whitespace
newlang5.asm.out: newlang5asm.py ../newlang5.newlang5 metaii_base.py
	python3 newlang5asm.py < ../newlang5.newlang5 > newlang5.asm.out
	$(DIFF) -w ../newlang5.out newlang5.asm.out


