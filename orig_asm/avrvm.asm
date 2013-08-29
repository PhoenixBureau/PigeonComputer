
.nolist
.include "m328Pdef.inc"
.list
.listmac

.def TOS = r27 ; XH
.def TOSL = r26 ; XL

.def Working = r16

.def word_counter = r17

.def Base = r8

.def number_pointer = r9

.def find_buffer_char = r10
.def find_name_char = r11

.def temp_length = r12

.def twi = r18

.dseg
.org SRAM_START

buffer: .byte 0x40

data_stack: .org 0x0140 ; SRAM_START + buffer

.MACRO popup
  ld TOSL, -Y
.ENDMACRO

.MACRO pushdownw
  st Y+, TOSL
  st Y+, TOS
.ENDMACRO

.MACRO popupw
  ld TOS, -Y
  ld TOSL, -Y
.ENDMACRO

.cseg

.org 0x0000
  jmp RESET
  jmp BAD_INTERUPT ; INT0 External Interrupt Request 0
  jmp BAD_INTERUPT ; INT1 External Interrupt Request 1
  jmp BAD_INTERUPT ; PCINT0 Pin Change Interrupt Request 0
  jmp BAD_INTERUPT ; PCINT1 Pin Change Interrupt Request 1
  jmp BAD_INTERUPT ; PCINT2 Pin Change Interrupt Request 2
  jmp BAD_INTERUPT ; WDT Watchdog Time-out Interrupt
  jmp BAD_INTERUPT ; TIMER2 COMPA Timer/Counter2 Compare Match A
  jmp BAD_INTERUPT ; TIMER2 COMPB Timer/Counter2 Compare Match B
  jmp BAD_INTERUPT ; TIMER2 OVF Timer/Counter2 Overflow
  jmp BAD_INTERUPT ; TIMER1 CAPT Timer/Counter1 Capture Event
  jmp BAD_INTERUPT ; TIMER1 COMPA Timer/Counter1 Compare Match A
  jmp BAD_INTERUPT ; TIMER1 COMPB Timer/Coutner1 Compare Match B
  jmp BAD_INTERUPT ; TIMER1 OVF Timer/Counter1 Overflow
  jmp BAD_INTERUPT ; TIMER0 COMPA Timer/Counter0 Compare Match A
  jmp BAD_INTERUPT ; TIMER0 COMPB Timer/Counter0 Compare Match B
  jmp BAD_INTERUPT ; TIMER0 OVF Timer/Counter0 Overflow
  jmp BAD_INTERUPT ; SPI, STC SPI Serial Transfer Complete
  jmp BAD_INTERUPT ; USART, RX USART Rx Complete
  jmp BAD_INTERUPT ; USART, UDRE USART, Data Register Empty
  jmp BAD_INTERUPT ; USART, TX USART, Tx Complete
  jmp BAD_INTERUPT ; ADC ADC Conversion Complete
  jmp BAD_INTERUPT ; EE READY EEPROM Ready
  jmp BAD_INTERUPT ; ANALOG COMP Analog Comparator
  jmp BAD_INTERUPT ; TWI 2-wire Serial Interface
  jmp BAD_INTERUPT ; SPM READY Store Program Memory Ready
BAD_INTERUPT:
  jmp 0x0000

RESET:
  cli

ldi Working, low(RAMEND)
out SPL, Working
ldi Working, high(RAMEND)
out SPH, Working

ldi YL, low(data_stack)
ldi YH, high(data_stack)

rcall UART_INIT

ldi Working, 23
sts TWBR, Working ; set bitrate
ldi Working, 1
sts TWSR, Working ; set prescaler

ldi Working, 10
mov Base, Working

sei

MAIN:
  rcall INTERPRET_PFA
  rcall DOTESS_PFA
  rjmp MAIN

UART_INIT:
  ldi r17, high(520) ; 2400 baud w/ 20Mhz osc
  ldi r16, low(520)  ; See Datasheet
  sts UBRR0H, r17
  sts UBRR0L, r16
  ; The chip defaults to 8N1 so we won't set it here even though we
  ; should.
  ldi r16, (1 << TXEN0) | (1 << RXEN0) ; Enable transmit/receive
  sts UCSR0B, r16
  ret

KEY:
  .dw 0x0000
  .db 3, "key"

KEY_PFA:
  lds Working, UCSR0A
  sbrs Working, RXC0
  rjmp KEY_PFA

rcall DUP_PFA
lds TOS, UDR0

rcall ECHO_PFA
ret

DUP:
  .dw KEY
  .db 3, "dup"
DUP_PFA:
  st Y+, TOSL ; push TOSL onto data stack
  mov TOSL, TOS
  ret

EMIT:
  .dw DUP
  .db 4, "emit"
EMIT_PFA:
  rcall ECHO_PFA
  rcall DROP_PFA
  ret

ECHO:
  .dw EMIT
  .db 4, "echo"

ECHO_PFA:
  lds Working, UCSR0A
  sbrs Working, UDRE0
  rjmp ECHO_PFA

sts UDR0, TOS
ret

DROP:
  .dw ECHO
  .db 4, "drop"
DROP_PFA:
  mov TOS, TOSL
  popup
  ret

WORD:
  .dw DROP
  .db 4, "word"
WORD_PFA:

rcall KEY_PFA

cpi TOS, ' '
brne _a_key

rcall DROP_PFA
rjmp WORD_PFA

_a_key:
  ldi ZL, low(buffer)
  ldi ZH, high(buffer)
  ldi word_counter, 0x00

_find_length:
  cpi word_counter, 0x40
  breq _a_key

st Z+, TOS
rcall DROP_PFA
inc word_counter

rcall KEY_PFA
cpi TOS, ' '
brne _find_length

mov TOS, word_counter
ret

NUMBER:
  .dw WORD
  .db 6, "number"
NUMBER_PFA:

ldi ZL, low(buffer)
ldi ZH, high(buffer)

mov number_pointer, TOS
ldi Working, 0x00
ld TOS, Z+
rjmp _convert

_convert_again:
  mul Working, Base
  mov Working, r0
  ld TOS, Z+

_convert:

cpi TOS, '0'
brlo _num_err
cpi TOS, ':' ; the char after '9'
brlo _decimal

rjmp _num_err

_decimal:
  subi TOS, '0'
  rjmp _converted

_num_err:
  st Y+, TOSL
  mov TOSL, TOS
  mov TOS, number_pointer
  ret

_converted:
  add Working, TOS
  dec number_pointer
  brne _convert_again

st Y+, TOSL
mov TOSL, Working
mov TOS, number_pointer
ret

LEFT_SHIFT_WORD:
  .dw NUMBER
  .db 3, "<<w"
LEFT_SHIFT_WORD_PFA:
  mov Working, TOS
  clr TOS
  lsl TOSL

  brcc _lslw0
  inc TOS ; copy carry flag to TOS[0]
_lslw0:
  lsl Working
  or TOS, Working

ret

HEXDIGITS: .db "0123456789abcdef"

EMIT_HEX:
  .dw LEFT_SHIFT_WORD
  .db 7, "emithex"
EMIT_HEX_PFA:

push ZH
push ZL

rcall DUP_PFA
swap TOS
rcall emit_nibble ; high
rcall emit_nibble ; low

pop ZL
pop ZH
ret

emit_nibble:

pushdownw
ldi TOS, high(HEXDIGITS)
ldi TOSL, low(HEXDIGITS)
rcall LEFT_SHIFT_WORD_PFA
movw Z, X
popupw

andi TOS, 0x0f

_eloop:
  cpi TOS, 0x00

breq _edone
dec TOS

  adiw Z, 1
  rjmp _eloop

_edone:

lpm TOS, Z
rcall EMIT_PFA
ret

DOTESS:
  .dw EMIT_HEX
  .db 2, ".s"
DOTESS_PFA:

rcall DUP_PFA

ldi TOS, 0x0d ; CR
rcall ECHO_PFA
ldi TOS, 0x0a ; LF
rcall ECHO_PFA
ldi TOS, '['
rcall ECHO_PFA

mov TOS, TOSL
rcall EMIT_HEX_PFA

mov Working, TOSL
rcall DUP_PFA      ; tos, tos, tosl
mov TOS, Working   ; tosl, tos, tosl
rcall DUP_PFA      ; tosl, tosl, tos, tosl
ldi TOS, '-'       ; '-', tosl, tos, tosl
rcall EMIT_PFA     ; tosl, tos, tosl
rcall EMIT_HEX_PFA ; tos, tosl

rcall DUP_PFA  ; tos, tos, tosl
ldi TOS, ' '   ; ' ', tos, tosl
rcall EMIT_PFA ; tos, tosl

  movw Z, Y
  rcall DUP_PFA

_inny:

ldi Working, low(data_stack)
cp ZL, Working
ldi Working, high(data_stack)
cpc ZH, Working
brsh _itsok

ldi TOS, ']'
rcall ECHO_PFA
ldi TOS, 0x0d ; CR
rcall ECHO_PFA
ldi TOS, 0x0a ; LF
rcall EMIT_PFA
ret

_itsok:
  ld TOS, -Z
  rcall EMIT_HEX_PFA
  rcall DUP_PFA
  ldi TOS, ' '
  rcall ECHO_PFA

rjmp _inny

FIND:
  .dw DOTESS
  .db 4, "find"
FIND_PFA:

mov word_counter, TOS
st Y+, TOSL
ldi TOSL, low(READ_IMU)
ldi TOS, high(READ_IMU)

_look_up_word:
  cpi TOSL, 0x00
  brne _non_zero
  cpse TOSL, TOS
  rjmp _non_zero

ldi TOS, 0xff
ldi TOSL, 0xff
ret

_non_zero:

pushdownw

rcall LEFT_SHIFT_WORD_PFA
movw Z, X
lpm TOSL, Z+
lpm TOS, Z+

lpm Working, Z+
cp Working, word_counter
breq _same_length

sbiw Y, 2
rjmp _look_up_word

_same_length:
  pushdownw
  ldi TOS, high(buffer)
  ldi TOSL, low(buffer)

_compare_name_and_target_byte:
  ld find_buffer_char, X+ ; from buffer
  lpm find_name_char, Z+ ; from program RAM
  cp find_buffer_char, find_name_char
  breq _okay_dokay

popupw ; ditch search term address
sbiw Y, 2 ; ditch LFA_current
rjmp _look_up_word

_okay_dokay:
  dec Working
  brne _compare_name_and_target_byte

popupw ; ditch search term address
popupw ; ditch LFA_next
ret ; LFA_current

TPFA:
  .dw FIND
  .db 4, ">pfa"
TPFA_PFA:

adiw X, 1
pushdownw ; save address
rcall LEFT_SHIFT_WORD_PFA

movw Z, X
lpm Working, Z
popupw ; restore address

  lsr Working
  inc Working       ; n <- (n >> 1) + 1
  add TOSL, Working ; Add the adjusted name length to our prog mem pointer.
  brcc _done_adding
  inc TOS           ; Account for the carry bit if set.
_done_adding:
  ret

INTERPRET:
  .dw TPFA
  .db 9, "interpret"
INTERPRET_PFA:

rcall WORD_PFA

mov temp_length, TOS

rcall NUMBER_PFA
cpi TOS, 0x00 ; all chars converted?
brne _maybe_word

mov TOS, TOSL
popup
ret

_maybe_word:
  mov TOS, temp_length
  popup
  rcall FIND_PFA

cpi TOS, 0xff
brne _is_word

popup
ldi TOS, '?'
rcall EMIT_PFA
ret

_is_word:
  rcall TPFA_PFA
  movw Z, X
  popupw
  ijmp

PB4_OUT:
  .dw INTERPRET
  .db 4, "pb4o"
PB4_OUT_PFA:

sbi DDRB, DDB4

sbi PORTB, PORTB4
ret

PB4_TOGGLE:
  .dw PB4_OUT
  .db 4, "pb4t"
PB4_TOGGLE_PFA:
  sbi PINB, PINB4
  ret

M1_ON:
  .dw PB4_TOGGLE
  .db 4, "m1on"
M1_ON_PFA:
  ldi Working, 0b11110011
  out TCCR0A, Working
  ldi Working, 0b00000010
  out TCCR0B, Working
  clr Working
  out OCR0A, Working
  out OCR0B, Working
  sbi DDRD, DDD5
  sbi DDRD, DDD6
  ret

M1_FORWARD:
  .dw M1_ON
  .db 3, "m1f"
M1_FORWARD_PFA:
  clr Working
  out OCR0A, Working
  out OCR0B, TOS
  ret

M1_REVERSE:
  .dw M1_FORWARD
  .db 3, "m1r"
M1_REVERSE_PFA:
  clr Working
  out OCR0B, Working
  out OCR0A, TOS
  ret

M2_ON:
  .dw M1_REVERSE
  .db 4, "m2on"
M2_ON_PFA:
  ldi Working, 0b11110011
  sts TCCR2A, Working
  ldi Working, 0b00000010
  sts TCCR2B, Working
  clr Working
  sts OCR2A, Working
  sts OCR2B, Working
  sbi DDRD, DDD3
  sbi DDRB, DDB3
  ret

M2_FORWARD:
  .dw M2_ON
  .db 3, "m2f"
M2_FORWARD_PFA:
  clr Working
  sts OCR2A, Working
  sts OCR2B, TOS
  ret

M2_REVERSE:
  .dw M2_FORWARD
  .db 3, "m2r"
M2_REVERSE_PFA:
  clr Working
  sts OCR2B, Working
  sts OCR2A, TOS
  ret

READ_ANALOG:
  .dw M2_REVERSE
  .db 7, "analog>"
READ_ANALOG_PFA:

ldi Working, 0b10000111
sts ADCSRA, Working

andi TOS, 0b00000111 ; mask to the first eight analog sources
ldi Working, 0b01100000
or Working, TOS
sts ADMUX, Working

ldi Working, 0b10000111 | (1 << ADSC)
sts ADCSRA, Working

_anindone:
  lds Working, ADCSRA
  sbrc Working, ADSC
  rjmp _anindone

lds TOS, ADCH
ret

.EQU TWI_START = 0x08
.EQU TWI_RSTART = 0x10
.EQU TWI_SLA_ACK = 0x18
.EQU TWI_SLA_NACK = 0x20
.EQU TWI_DATA_ACK = 0x28
.EQU TWI_ARB_LOST = 0x38
.EQU TWI_SLAR_ACK = 0x40

.EQU MAG_ADDRESS = 0b0011110 << 1 ; shift to make room for R/W bit
.EQU MR_REG_M = 0x02

.EQU ACCEL_ADDRESS = 0b0011000 << 1 ; shift to make room for R/W bit
.EQU CTRL_REG1_A = 0x20 ; set to 0b00100111 see datasheet
.EQU CTRL_REG4_A = 0x23 ; set to 0b10000000 see datasheet

.EQU GYRO_ADDRESS = 0b1101001 << 1 ; shift to make room for R/W bit
.EQU GYRO_CTRL_REG1 = 0x20

_twinty:
  lds Working, TWCR
  sbrs Working, TWINT
  rjmp _twinty
  ret

_twohno:
  rcall DUP_PFA
  ldi TOS, '!'
  rcall EMIT_PFA
  ret

.MACRO check_twi
  cpi twi, 0x00
  brne _twi_fail
.ENDMACRO

AFTER_SLA_W:
  rcall FETCH_TWSR
  rcall EXPECT_TWI_SLA_ACK
  rcall TWI_OR
  rcall EXPECT_TWI_SLA_NACK
  rcall TWI_OR
  rcall EXPECT_TWI_ARB_LOST
  ret

Send_START:
  check_twi
  ldi Working, (1 << TWINT)|(1 << TWSTA)|(1 << TWEN)
  sts TWCR, Working
  ret

Send_STOP:
  check_twi
  ldi Working, (1 << TWINT)|(1 << TWEN)|(1 << TWSTO)
  sts TWCR, Working
  ret

Send_BYTE:
  check_twi
  sts TWDR, Working
  ldi Working, (1 << TWINT)|(1 << TWEN)
  sts TWCR, Working
  ret

ENABLE_ACK_TWI: ; Needed to receive bytes
  ldi Working, (1 << TWINT)|(1 << TWEA)|(1 << TWEN)
  sts TWCR, Working
  ret

Receive_BYTE_TWI:
  rcall DUP_PFA
  lds TOS, TWDR
  ret

Send_NACK:
  ldi Working, (1 << TWINT)|(1 << TWEN)
  sts TWCR, Working
  ret

FETCH_TWSR:
  lds Working, TWSR
  andi Working, 0b11111000 ; mask non-status bytes
  ret

TWI_OR:
  cpi twi, 0x00  ; if success
  breq _twi_fail ; exit the calling routine
  ldi twi, 0     ; otherwise continue
  ret
_twi_fail:
  pop Working
  pop Working ; remove caller's return location from the return stack
  ret

EXPECT_TWI_START:
  check_twi
  cpi Working, TWI_START
  brne _twi_false
  ret

EXPECT_TWI_RSTART:
  check_twi
  cpi Working, TWI_RSTART
  brne _twi_false
  ret

EXPECT_TWI_SLA_ACK:
  check_twi
  cpi Working, TWI_SLA_ACK
  brne _twi_false
  ret

EXPECT_TWI_DATA_ACK:
  check_twi
  cpi Working, TWI_DATA_ACK
  brne _twi_false
  ret

EXPECT_TWI_SLA_NACK:
  check_twi
  cpi Working, TWI_SLA_NACK
  brne _twi_false
  ; this is a fail
  ldi twi, TWI_SLA_NACK ; mark failure
  rjmp _twi_fail ; exit caller

EXPECT_TWI_SLAR_ACK:
  check_twi
  cpi Working, TWI_SLAR_ACK
  brne _twi_false
  ret

EXPECT_TWI_ARB_LOST:
  check_twi
  cpi Working, TWI_ARB_LOST
  brne _twi_false
  ; this is a fail
  ldi twi, TWI_ARB_LOST ; mark failure
  rjmp _twi_fail ; exit caller

_twi_false:
  ldi twi, 1
  ret

_twi_start:
  rcall Send_START
  rcall _twinty
  rcall FETCH_TWSR
  ret

TWI_START_it:
  rcall _twi_start
  rcall EXPECT_TWI_START
  ret

TWI_RSTART_it:
  rcall _twi_start
  rcall EXPECT_TWI_RSTART
  ret

TWI_RECV_BYTE:
  rcall ENABLE_ACK_TWI
  rcall _twinty
  rcall Receive_BYTE_TWI
  ret

TWI_SEND_BYTE:
  rcall Send_BYTE
  rcall _twinty
  rcall FETCH_TWSR
  rcall EXPECT_TWI_DATA_ACK
  ret

SET_MAGNETOMETER_MODE:
  .dw READ_ANALOG
  .db 4, "IMAG"
SET_MAGNETOMETER_MODE_PFA:

    ldi twi, 0x00

    rcall TWI_START_it

    ldi Working, MAG_ADDRESS ; Magnetometer Address
    rcall Send_BYTE
    rcall _twinty
    rcall AFTER_SLA_W

    ldi Working, MR_REG_M ; Subaddress
    rcall TWI_SEND_BYTE

    ldi Working, 0x00 ; Write Mode
    rcall TWI_SEND_BYTE

    rcall Send_STOP
    ret


READ_MAGNETOMETER:
  .dw SET_MAGNETOMETER_MODE
  .db 4, "RMAG"
READ_MAGNETOMETER_PFA:

    ldi twi, 0x00

    rcall TWI_START_it

    ldi Working, MAG_ADDRESS ; Magnetometer Address
    rcall Send_BYTE
    rcall _twinty
    rcall AFTER_SLA_W

    ldi Working, 0x03 | 0b10000000 ; first data byte | auto-increment
    rcall TWI_SEND_BYTE

    rcall TWI_RSTART_it ; Repeated Start

    ldi Working, (MAG_ADDRESS | 1) ; Load Magnetometer Address with read bit
    rcall Send_BYTE
    rcall _twinty
    rcall FETCH_TWSR
    rcall EXPECT_TWI_SLAR_ACK ; SLA+R

    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE

    rcall Send_NACK
    rcall _twinty

    rcall Send_STOP
    ret

SET_ACCELEROMETER_MODE:
  .dw SET_MAGNETOMETER_MODE
  .db 4, "IACC"
SET_ACCELEROMETER_MODE_PFA:

    ldi twi, 0x00

    rcall TWI_START_it

    ldi Working, ACCEL_ADDRESS
    rcall Send_BYTE
    rcall _twinty
    rcall AFTER_SLA_W

    ldi Working, CTRL_REG1_A ; Subaddress
    rcall TWI_SEND_BYTE

    ldi Working, 0b00100111 ; Write Value
    rcall TWI_SEND_BYTE

    rcall Send_STOP
    ret


READ_ACCELEROMETER:
  .dw SET_ACCELEROMETER_MODE
  .db 4, "RACC"
READ_ACCELEROMETER_PFA:

    ldi twi, 0x00

    rcall TWI_START_it

    ldi Working, ACCEL_ADDRESS
    rcall Send_BYTE
    rcall _twinty
    rcall AFTER_SLA_W

    ldi Working, 0x28 | 0b10000000 ; first data byte | auto-increment
    rcall TWI_SEND_BYTE

    rcall TWI_RSTART_it ; Repeated Start

    ldi Working, (ACCEL_ADDRESS | 1) ; address with read bit
    rcall Send_BYTE
    rcall _twinty
    rcall FETCH_TWSR
    rcall EXPECT_TWI_SLAR_ACK ; SLA+R

    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE

    rcall Send_NACK
    rcall _twinty

    rcall Send_STOP
    ret




SET_GYRO_MODE:
  .dw READ_ACCELEROMETER
  .db 5, "IGYRO"
SET_GYRO_MODE_PFA:

    ldi twi, 0x00

    rcall TWI_START_it

    ldi Working, GYRO_ADDRESS
    rcall Send_BYTE
    rcall _twinty
    rcall AFTER_SLA_W

    ldi Working, GYRO_CTRL_REG1 ; Subaddress
    rcall TWI_SEND_BYTE

    ldi Working, 0b00001111 ; Write Value
    rcall TWI_SEND_BYTE

    rcall Send_STOP
    ret

READ_GYRO:
  .dw SET_GYRO_MODE
  .db 5, "RGYRO"
READ_GYRO_PFA:

    ldi twi, 0x00

    rcall TWI_START_it

    ldi Working, GYRO_ADDRESS
    rcall Send_BYTE
    rcall _twinty
    rcall AFTER_SLA_W

    ldi Working, 0x28 | 0b10000000 ; first data byte | auto-increment
    rcall TWI_SEND_BYTE

    rcall TWI_RSTART_it ; Repeated Start

    ldi Working, (GYRO_ADDRESS | 1) ; address with read bit
    rcall Send_BYTE
    rcall _twinty
    rcall FETCH_TWSR
    rcall EXPECT_TWI_SLAR_ACK ; SLA+R

    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE
    rcall TWI_RECV_BYTE

    rcall Send_NACK
    rcall _twinty

    rcall Send_STOP
    ret


READ_IMU:
  .dw READ_GYRO
  .db 4, "RIMU"
READ_IMU_PFA:
  rcall READ_GYRO_PFA
  ldi word_counter, 6
  rcall _send_imu_bytes

  rcall READ_MAGNETOMETER_PFA
  ldi word_counter, 6
  rcall _send_imu_bytes

  rcall READ_ACCELEROMETER_PFA
  ldi word_counter, 6
  rcall _send_imu_bytes
  ret

_send_imu_bytes:
  rcall EMIT_HEX_PFA
  dec word_counter
  brne _send_imu_bytes
  ret
