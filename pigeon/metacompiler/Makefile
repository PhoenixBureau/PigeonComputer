.SUFFIXES :
DIFF = diff --report-identical-files
PATCH = patch --quiet -V none

# newlang

# It seems I have already altered metaii.metaii to recognize '«' and '»'
# in lieu of '.OUT(' and ')', so that metaii.asm and newlang.asm are not
# identical!  It doesn't use them though. The compiler defined by
# newlang.asm will recognize them.
newlang.asm: metaii.py metaii.asm metaii.metaii
	python3 metaii.py -p metaii.asm metaii.metaii > newlang.asm

# Modify the metaii.metaii to use the new '«' and '»' syntax.
newlang.newlang: metaii.metaii sed_command
	sed -f sed_command < metaii.metaii > newlang.newlang

# The two files newlang.asm and newlang.newlang define a metacompiler.
newlang.out: metaii.py newlang.asm newlang.newlang
	python3 metaii.py -p newlang.asm newlang.newlang  > newlang.out
	$(DIFF) newlang.asm newlang.out

# newlang0

# To get from newlang.newlang to newlang0.newlang we alter the syntax to
# recognize (but not yet use) a star instead of a dollar sign for the
# Kleene Star zero-or-more meta-pattern.
newlang0.newlang: newlang.newlang
	# I can't figure out how to quote "'$'" on the CLI, I originaly
	# used a text editor.  TODO: use sed or something?
	echo "newlang.newlang -> newlang0.newlang"
	touch newlang0.newlang

# Generate a compiler that recognizes newlang0.
newlang0.asm: metaii.py newlang.out newlang0.newlang
	python3 metaii.py -p newlang.out newlang0.newlang > newlang0.asm

# Replace $ with ★ in the grammar.
newlang0.newlang0: newlang0.newlang
	sed 's/\$$/★/' < newlang0.newlang > newlang0.newlang0

# Use the compiler is a metacompiler.
newlang0.out: metaii.py newlang0.asm newlang0.newlang0
	python3 metaii.py -p newlang0.asm newlang0.newlang0 > newlang0.out
	$(DIFF) newlang0.asm newlang0.out

# newlang1

newlang1.newlang0: newlang0.newlang0 newlang0-1.diff
	$(PATCH) -o newlang1.newlang0 -i newlang0-1.diff newlang0.newlang0

newlang1.asm: metaii.py newlang0.out newlang1.newlang0
	python3 metaii.py -p newlang0.out newlang1.newlang0 > newlang1.asm

newlang1.newlang1: sed_command1 newlang1.newlang0
	sed -f sed_command1 < newlang1.newlang0 > newlang1.newlang1

newlang1.out: newlang1.asm newlang1.newlang1
	python3 metaii.py -p newlang1.asm newlang1.newlang1 > newlang1.out
	$(DIFF) newlang1.asm newlang1.out

# newlang2

newlang2.newlang1: newlang1.newlang1 newlang1-2.diff
	$(PATCH) -o newlang2.newlang1 -i newlang1-2.diff newlang1.newlang1

newlang2.asm: metaii.py newlang1.out newlang2.newlang1
	python3 metaii.py -p newlang1.out newlang2.newlang1 > newlang2.asm

newlang2.newlang2: newlang2.newlang1 sed_command2
	sed -f sed_command2 < newlang2.newlang1 > newlang2.newlang2

newlang2.out: metaii.py newlang2.asm newlang2.newlang2
	python3 metaii.py -p newlang2.asm newlang2.newlang2 > newlang2.out
	$(DIFF) newlang2.asm newlang2.out

# newlang3

newlang3.newlang2: newlang2.newlang2 newlang2-3.diff
	$(PATCH) -o newlang3.newlang2 -i newlang2-3.diff newlang2.newlang2

newlang3.asm: metaii.py newlang2.out newlang3.newlang2
	python3 metaii.py -p newlang2.out newlang3.newlang2 > newlang3.asm

newlang3.newlang3: newlang3.newlang2 sed_command3
	sed -f sed_command3 < newlang3.newlang2 > newlang3.newlang3

newlang3.out: metaii.py newlang3.asm newlang3.newlang3
	python3 metaii.py -p newlang3.asm newlang3.newlang3 > newlang3.out
	$(DIFF) newlang3.asm newlang3.out

# newlang4

newlang4.newlang3: newlang3.newlang3 newlang3-4.diff
	$(PATCH) -o newlang4.newlang3 -i newlang3-4.diff newlang3.newlang3

newlang4.asm: metaii.py newlang3.out newlang4.newlang3
	python3 metaii.py -p newlang3.out newlang4.newlang3 > newlang4.asm

newlang4.out: metaii.py newlang4.asm newlang4.newlang3
	python3 metaii.py -p newlang4.asm newlang4.newlang3 > newlang4.out
	$(DIFF) newlang4.asm newlang4.out

# newlang5

newlang5.newlang4: newlang4.newlang4 newlang4-5.diff
	$(PATCH) -o newlang5.newlang4 -i newlang4-5.diff newlang4.newlang4

newlang5.asm: metaii.py newlang4.asm newlang5.newlang4
	python3 metaii.py -p newlang4.asm newlang5.newlang4 > newlang5.asm

newlang5.newlang5: newlang5.newlang4 newlang4-5.diff
	$(PATCH) -o newlang5.newlang5 -i newlang4-5.diff newlang5.newlang4

newlang5.out: metaii.py newlang5.asm newlang5.newlang5
	python3 metaii.py   -p newlang5.asm newlang5.newlang5 > newlang5.out

newlang5.outt: metaii.5.py newlang5.out newlang5.newlang5
	python3 metaii.5.py -p newlang5.out newlang5.newlang5 > newlang5.outt

newlang5py.py.out: newlang5py.py newlang5py.newlang5
	python3 newlang5py.py < newlang5py.newlang5 > newlang5py.py.out

newlang5py.asm: metaii.5.py newlang5.out newlang5py.newlang5
	python3 metaii.5.py -p newlang5.out newlang5py.newlang5 > newlang5py.asm

newlang5py.py: metaii.5.py newlang5py.asm newlang5py.newlang5
	python3 metaii.5.py -p newlang5py.asm newlang5py.newlang5 > newlang5py.py

newlang5asm.py: newlang5py.py newlang5.newlang5
	python3 newlang5py.py < newlang5.newlang5 > newlang5asm.py

newlang5.asm.out: newlang5asm.py newlang5.newlang5
	python3 newlang5asm.py < newlang5.newlang5 > newlang5.asm.out

