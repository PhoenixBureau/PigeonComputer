Pigeon Computer
===============

Simple computer system built around ATmega328P microcontroller.

Right now there is just a simple assembler, written in Python, for the AVR
assembly language.  It is built along the ideas of Miki Tebeka  and his
fascinating [Python based assembler][1] although with a slightly
different architecture.  The basic trick of interpreting a python file
in a special context to get parsing &c. for free is the same.


The following instructions are implemented so far:

* add
* adiw
* andi
* brcc
* breq
* brlo
* brne
* brsh
* cli
* clr
* cp
* cpc
* cpi
* cpse
* dec
* ijmp
* inc
* jmp
* ld_post_incr
* ld_pre_decr
* ldi
* lds
* lpm
* lpm_post_incr
* lsl
* lsr
* mov
* movw
* mul
* or_
* out
* pop
* push
* rcall
* ret
* rjmp
* sbiw
* sbrs
* sei
* st_post_incr
* sts
* subi
* swap


### Dependencies

* MyHDL
* IntelHex
* (eventually) pexpect


[1]: http://pythonwise.blogspot.com/2012/06/python-based-assembler.html

