.SUFFIXES :
DIFF = diff --report-identical-files

all: metaii.out

metaii.out: metaii.py metaii.asm  metaii.metaii
	./metaii.py -p metaii.asm metaii.metaii > metaii.out
	$(DIFF) metaii.asm metaii.out

clean:
	rm -vf metaii.out
