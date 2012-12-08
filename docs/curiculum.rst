==========================
What is a Computer Anyway?
==========================


Unlike Magnets, Computers *can* be Explained
--------------------------------------------


The Bit
---------------

Make a One-bit memory.

I'm seriously here, your first lesson is to make a device, no matter how
simple, that stores one bit. It can be:

- A coin, flip heads for 1, tails for 0.
- A match, horizontal or vertical, head up or head down...
- A short length of string, knotted for 0, untied for 1.
- A rubber-band, knotted for 1, unknotted for 0.
- A business card, horiz. v. vert., front v. back, bent v. straightened.
- Even a light switch from a hardware store.

Literally any binary "storage" scheme could be accepted, as long as the
student truly gets the arbitrary mapping from a physical phenomenon to a
binary digit. I am convinced that doing this physically, with real world
objects, is crucial. Take your time here, don't rush. The binary digit is
a deep sucker, it just seems so plain on first brush. (Hint: What is the
least "stuff" you need to make a bit? Sample rate and resolution... What
the heck "is" a bit anyway? You can't carry it, but you can transmit it,
what's up with that? And you can duplicate it? Huh?)


Line up eight of them. Make a byte.
-----------------------------------

Once you've made a bit-store, the next lesson involves lining them up and
flipping them on and off.

Count the states, number them, talk about:

- n-to-the-power-of-two
- Grey Codes
- I Ching
- distinguishable states
- Boolean logic
- all the deep meanings already present in more-than-one-bit-ness. (Twenty Questions!)

Make concrete the Octet, aka Byte, mention ASCII, signed and unsigned
"short" ints, Unicode and encodings (to bytes) and thence sixteen-bit and
larger words.


Stack up a bunch of bytes. Make RAM.
------------------------------------

- Take some bytes, at least a dozen, and stack them in a column. Count
  the bytes, introduce the count as naming or indexing the bytes, call it
  RAM.
- Show how a few consecutive bytes of RAM can store a string of ASCII
  codes.
- Do a couple of math problems using two adjacent bytes as (binary)
  operands and another byte to store the result.
- Move a couple of bytes from one area in the RAM to another.


Addresses, numbers, operations, naming. (microcode)
---------------------------------------------------

Wonder at the beauty and greatness of what we've done so far. We mapped
binary digits (bits) to real world phenomenon. We used a simple coding
system, algebra in base two, to encode the integers into bit patterns. We
created a "strip" or "column" of bits, organized in eight-bit-wide words
called bytes or octets, and then numbered those, counted them to name
them, and began to use this abacus-like crude machine of ours to perform
simple operations like math, logic, and "string" manipulation.


The Power of Naming
-------------------

Start to make the steps used to perform these operations more concrete.
Use index cards or something and list out the various steps you take in
performing a few simple math/logic problems and stuff.

Do the counting-to-name-things trick yet again to enumerate the
"microcode" you've developed, and lay in a simple program using it.

Act out the Fetch-Execute cycle and let people get used to the idea of
how simple it is. Maybe even assign each instruction of microcode to a
different person and have the class cooperatively act out the solving of
a simple math problem or two according to an in-memory machine language
program. (That will prove viscerally that you don't need a brain or mind
to "be" a computer. Put another way, some classes of mental operation can
be automated, carried out by machine.)

(You would also introduce the idea that RAM can be a lot larger than just
a dozen bytes or so, and likely mention registers too.)


Parsing, Grammar, Compiling.
----------------------------


Ahem, some about that and the Meta-Compiler...


