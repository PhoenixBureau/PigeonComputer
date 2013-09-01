Pigeon Computer
===============

A simple computer system built around the [ATmega328P microcontroller][1].

### From the Bare Bit to the Compiler, and Beyond...

It is designed to be easy to use and understand at a deep level.  It was
developed to support a very hands-on course on the foundations of
computers and programming, and as such it covers the core concepts that are
typically left out of classes on programming.

Within an elegant and powerful integrated development environment there
are:

* A simple assembler for the AVR assembly language.
* A compiler that is extremely easy to understand and extend so you can
  learn how compilers work and even develop your own custom high-level
  language(s).
* A simple and powerful Forth-like firmware that implements a
  command-line interpreter for the ATmega328P in less than a kilobyte.
* There is also some experimental support for running a simulator
  interactively, but it is still very tentative and unfinished and so
  is not included in this release.

### Links

Currently the source code is hosted on [GitHub][3] where you can download
it, report bugs, contribute to or just fork it (it's open source under
the GPL, see the `COPYING` file in the source.)

In addition to reading the source you should read the [Manual (online
HTML version)][4] (This is still in a very rough draft stage with missing
sections still to be filled in but I'm actively improving it.)

### Dependencies and Working Environment

If you have Python (and Tkinter) installed then the only dependencies are:

* MyHDL
* IntelHex http://www.bialix.com/intelhex/ http://pypi.python.org/pypi/IntelHex/1.4
* Dulwich https://www.samba.org/~jelmer/dulwich/ http://pypi.python.org/pypi/dulwich

It is recommended to use Pip and Virtualenv to set up the working environment.
Start in the toplevel directory, set up a virtual environment, install MyHDL
(for some reason it's not on PyPI at the time of this writing) and then use
Pip to install the rest of the requirements automatically:

    virtualenv virt-env
    source ./virt-env/bin/activate
    cd thirdparty
    tar xzf myhdl-0.7.tar.gz
    cd myhdl-0.7
    python setup.py install
    cd ..
    rm -rf myhdl-0.7
    cd ..
    pip install -r requirements.text 

Then run with:

    python -m pigeon --init

(Leave off the "--init" switch after the first time, it just initializes
the "roost" directory and isn't needed except for the first time you run
the program.)

The system will use a "roost" directory to store your saved history. The
default directory is `$HOME/.pigeon` but you can choose another location
with the "--roost" switch.


#### Generating the Pigeon Firmware ASM File (Optional)

The Pigeon Firmware is written as a reStructuredText document and then
converted into a source file for the Pigeon Assembler using a utility
script.  You don't have to do this yourself as a copy of the extracted
assembly source file is already included as `assembler/asm.py`, but it's
good to know how that file gets made in case you want to modify it
yourself.

To generate the asm.py file from the pigeon_firmware.rst file use the
`rest2asm.py` script in the `assembler` subdirectory:

    cd assembler
    ./rest2asm.py ../docs/pigeon_firmware.rst > asm.py 


[1]: http://www.atmel.com/devices/atmega328p.aspx

[2]: http://pythonwise.blogspot.com/2012/06/python-based-assembler.html

[3]: https://github.com/PhoenixBureau/PigeonComputer

[4]: http://phoenixbureau.github.com/PigeonComputer/
