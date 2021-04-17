To change the syntax in the newlang.newlang I used sed:

    % cat sed_command 
    s/.OUT(\([A-Z0-9'* ]*\))/«\1»/g

    % sed -i '' -f sed_command newlang.newlang



    s/.OUT(   \( [A-Z0-9'* ]* \)     ) / «\1» /g
      ^^^^^   ^^ ^^^^^^^^^^^^ ^^     ^    ^^
       lit | group | inner | group |lit| substitute inner 


### Run the compiler on the new syntax file:

    % python3 metaii.py -p newlang.asm newlang.newlang  > newlang.out
    % diff --report-identical-files newlang.asm newlang.out
    Files newlang.asm and newlang.out are identical


    % sed -i '' 's/$/★/' newlang0.newlang0
    % diff newlang0.newlang newlang0.newlang0
    ...
    % python3 metaii.py -p newlang0.asm newlang0.newlang0 > newlang0.out
    % diff  --report-identical-files newlang0.asm newlang0.out
    Files newlang0.asm and newlang0.out are identical




-------------------

python3 metaii.py -p newlang0.asm newlang1.newlang0 > newlang1.asm
cp newlang1.newlang0 newlang1.newlang1
git add newlang1.newlang1
git commit -m 'Pretty Unicode.'
sed -i '' -f sed_command1 newlang1.newlang1
python3 metaii.py -p newlang1.asm newlang1.newlang1 > newlang1.out
diff  --report-identical-files newlang1.asm newlang1.out
> Files newlang1.asm and newlang1.out are identical




c( newlang.asm,  newlang.newlang ) ->  newlang.asm
c( newlang.asm, newlang0.newlang ) -> newlang0.asm
c(newlang0.asm, newlang0.newlang0) -> newlang0.asm
c(newlang0.asm, newlang1.newlang0) -> newlang1.asm
c(newlang1.asm, newlang1.newlang1) -> newlang1.asm

Get the cadence?

Add new syntax from fooN.fooN to FooN+1.FooN
then use it to write FooN+1.FooN+1



python3 metaii.py -p newlang2.asm newlang2.newlang1 > newlang2.asm
cp newlang2.newlang1 newlang2.newlang2
git add newlang2.newlang2
git commit -m 'More Pretty Unicode.'
sed -i '' -f sed_command2 newlang2.newlang2
python3 metaii.py -p newlang2.asm newlang2.newlang2 > newlang2.out
diff  --report-identical-files newlang2.asm newlang2.out
Files newlang2.asm and newlang2.out are identical


----------------------
python3 metaii.py -p newlang1.asm newlang2.newlang1 > newlang2.asm
python3 metaii.py -p newlang2.asm newlang2.newlang2 > newlang2.out

----------------------

sed -i '' -f sed_command newlang3.newlang3

---------------------------------------------------


For the sematics output change I had to add new "asm" methods to the VM.




python3 metaii.py   -p newlang5.asm newlang5.newlang5 > newlang5.out
python3 metaii.5.py -p newlang5.out newlang5.newlang5 > newlang5.outt

% diff -sw newlang5.out newlang5.outt 
Files newlang5.out and newlang5.outt are identical


I know it's pointless but I find it amusing:

% python3 metaii.5.py -p newlang5.outtt newlang5.newlang5 > newlang5.outttt
% python3 metaii.5.py -p newlang5.outttt newlang5.newlang5 > newlang5.outtttt
% ls -l newlang5.ou*
-rw-r--r-- 1 sforman sforman 1497 Apr 16 13:39 newlang5.out
-rw-r--r-- 1 sforman sforman 2094 Apr 16 13:41 newlang5.outt
-rw-r--r-- 1 sforman sforman 2094 Apr 16 13:46 newlang5.outtt
-rw-r--r-- 1 sforman sforman 2094 Apr 16 13:46 newlang5.outttt
-rw-r--r-- 1 sforman sforman 2094 Apr 16 13:46 newlang5.outtttt


Anyhow, metaii.5.py and newlang5.newlang5 are a metacompiler
with "block structure" output capability.


                  ...


sforman@bock:~/src/PigeonComputer/pigeon/metacompiler % python3 metaii.5.py -p newlang5.out newlang5py.newlang5 > newlang5py.asm
sforman@bock:~/src/PigeonComputer/pigeon/metacompiler % python3 metaii.5.py -p newlang5py.asm newlang5py.newlang5 > newlang5py.py
sforman@bock:~/src/PigeonComputer/pigeon/metacompiler % python3 newlang5py.py < newlang5py.newlang5 > newlang5py.py.out
sforman@bock:~/src/PigeonComputer/pigeon/metacompiler % diff -s newlang5py.py newlang5py.py.out
Files newlang5py.py and newlang5py.py.out are identical


python3 newlang5py.py < newlang5.newlang5 > newlang5asm.py
python3 newlang5asm.py < newlang5.newlang5 > newlang5.asm.out

but there's an error, the label #'s aren't getting updated...
newlang5.asm.out is broken..

Ah, it's a misspelled variable name.
