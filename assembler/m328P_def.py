'''
The following definitions are taken from the m328Pdef.inc file available
from the Amtel corporation as part of the suite of software tools they
provide.

For details on any of these consult the Amtel manuals, et. al.
'''
from util import int2addr


def _f(n):
  if isinstance(n, str):
    n = int(n, 16)
  return int2addr(n)


_mark = set(dir())


# The following comment is from the Amtel m328Pdef.inc

#***** THIS IS A MACHINE GENERATED FILE - DO NOT EDIT ********************
#***** Created: 2010-08-20 14:22 ******* Source: ATmega328P.xml **********
#*************************************************************************
#* A P P L I C A T I O N   N O T E   F O R   T H E   A V R   F A M I L Y
#* 
#* Number            : AVR000
#* File Name         : "m328Pdef.inc"
#* Title             : Register/Bit Definitions for the ATmega328P
#* Date              : 2010-08-20
#* Version           : 2.35
#* Support E-mail    : avr@atmel.com
#* Target MCU        : ATmega328P
#* 
#* DESCRIPTION
#* When including this file in the assembly program file, all I/O register 
#* names and I/O register bit names appearing in the data book can be used.
#* In addition, the six registers forming the three data pointers X, Y and 
#* Z have been assigned names XL - ZH. Highest RAM address for Internal 
#* SRAM is also defined 
#* 
#* The Register names are represented by their hexadecimal address.
#* 
#* The Register Bit names are represented by their bit number (0-7).
#* 
#* Please observe the difference in using the bit names with instructions
#* such as "sbr"/"cbr" (set/clear bit in register) and "sbrs"/"sbrc"
#* (skip if bit in register set/cleared). The following example illustrates
#* this:
#* 
#* in    r16,PORTB             #read PORTB latch
#* sbr   r16,(1<<PB6)+(1<<PB5) #set PB6 and PB5 (use masks, not bit#)
#* out   PORTB,r16             #output to PORTB
#* 
#* in    r16,TIFR              #read the Timer Interrupt Flag Register
#* sbrc  r16,TOV0              #test the overflow flag (use bit#)
#* rjmp  TOV0_is_set           #jump if set
#* ...                         #otherwise do something else
#*************************************************************************


# ***** I/O REGISTER DEFINITIONS *****************************************
# NOTE:
# Definitions marked "MEMORY MAPPED"are extended I/O ports
# and cannot be used with IN/OUT instructions

#: USART I/O Data Register
UDR0	= '0xc6'	# MEMORY MAPPED

#: USART Baud Rate Register (low)
UBRR0L	= '0xc4'	# MEMORY MAPPED

#: USART Baud Rate Register (high)
UBRR0H	= '0xc5'	# MEMORY MAPPED

#: USART Control and Status Register C
UCSR0C	= '0xc2'	# MEMORY MAPPED

#: USART Control and Status Register B
UCSR0B	= '0xc1'	# MEMORY MAPPED

#: USART Control and Status Register A
UCSR0A	= '0xc0'	# MEMORY MAPPED

#: TWI (Slave) Address Mask Register
TWAMR	= '0xbd'	# MEMORY MAPPED

#: TWI Control Register
TWCR	= '0xbc'	# MEMORY MAPPED

#: TWI Data Register
TWDR	= '0xbb'	# MEMORY MAPPED

#: TWI (Slave) Address Register
TWAR	= '0xba'	# MEMORY MAPPED

#: TWI Status Register
TWSR	= '0xb9'	# MEMORY MAPPED

#: TWI Bit Rate Register
TWBR	= '0xb8'	# MEMORY MAPPED

#:
ASSR	= '0xb6'	# MEMORY MAPPED

#: Timer/Counter2 Output Compare Register B
OCR2B	= '0xb4'	# MEMORY MAPPED

#: Timer/Counter2 Output Compare Register A
OCR2A	= '0xb3'	# MEMORY MAPPED

#:
TCNT2	= '0xb2'	# MEMORY MAPPED

#:
TCCR2B	= '0xb1'	# MEMORY MAPPED

#:
TCCR2A	= '0xb0'	# MEMORY MAPPED

#:
OCR1BL	= '0x8a'	# MEMORY MAPPED

#:
OCR1BH	= '0x8b'	# MEMORY MAPPED

#:
OCR1AL	= '0x88'	# MEMORY MAPPED

#:
OCR1AH	= '0x89'	# MEMORY MAPPED

#:
ICR1L	= '0x86'	# MEMORY MAPPED

#:
ICR1H	= '0x87'	# MEMORY MAPPED

#:
TCNT1L	= '0x84'	# MEMORY MAPPED

#:
TCNT1H	= '0x85'	# MEMORY MAPPED

#:
TCCR1C	= '0x82'	# MEMORY MAPPED

#:
TCCR1B	= '0x81'	# MEMORY MAPPED

#:
TCCR1A	= '0x80'	# MEMORY MAPPED

#:
DIDR1	= '0x7f'	# MEMORY MAPPED

#: Digital Input Disable Register 0
DIDR0	= '0x7e'	# MEMORY MAPPED

#: ADC Multiplexer Selection Register
ADMUX	= '0x7c'	# MEMORY MAPPED

#: ADC Control and Status Register B
ADCSRB	= '0x7b'	# MEMORY MAPPED

#: ADC Control and Status Register A
ADCSRA	= '0x7a'	# MEMORY MAPPED

#: The ADC Data Register (high)
ADCH	= '0x79'	# MEMORY MAPPED

#: The ADC Data Register (low)
ADCL	= '0x78'	# MEMORY MAPPED

#:
TIMSK2	= '0x70'	# MEMORY MAPPED

#:
TIMSK1	= '0x6f'	# MEMORY MAPPED

#:
TIMSK0	= '0x6e'	# MEMORY MAPPED

#:
PCMSK1	= '0x6c'	# MEMORY MAPPED

#:
PCMSK2	= '0x6d'	# MEMORY MAPPED

#:
PCMSK0	= '0x6b'	# MEMORY MAPPED

#:
EICRA	= '0x69'	# MEMORY MAPPED

#:
PCICR	= '0x68'	# MEMORY MAPPED

#: Oscillator Calibration Register
OSCCAL	= '0x66'	# MEMORY MAPPED

#: Power Reduction Register
PRR	= '0x64'	# MEMORY MAPPED

#: Clock Prescale Register
CLKPR	= '0x61'	# MEMORY MAPPED

#: Watchdog Timer Control Register
WDTCSR	= '0x60'	# MEMORY MAPPED

#: Status Register
SREG	= '0x3f'

#: Stack Pointer (low)
SPL	= '0x3d'

#: Stack Pointer (high)
SPH	= '0x3e'

#: Store Program Memory Control and Status Register
SPMCSR	= '0x37'

#: MCU Control Register
MCUCR	= '0x35'

#: MCU Status Register
MCUSR	= '0x34'

#: Sleep Mode Control Register
SMCR	= '0x33'

#: Analog Comparator Control and Status Register
ACSR	= '0x30'

#:
SPDR	= '0x2e'

#:
SPSR	= '0x2d'

#:
SPCR	= '0x2c'

#:
GPIOR2	= '0x2b'

#:
GPIOR1	= '0x2a'

#: Timer/Counter2 Output Compare Register B
OCR0B	= '0x28'

#: Timer/Counter2 Output Compare Register A
OCR0A	= '0x27'

#:
TCNT0	= '0x26'

#:
TCCR0B	= '0x25'

#:
TCCR0A	= '0x24'

#:
GTCCR	= '0x23'

#: The EEPROM Address Register (high)
EEARH	= '0x22'

#: The EEPROM Address Register (low)
EEARL	= '0x21'

#: The EEPROM Data Register
EEDR	= '0x20'

#: The EEPROM Control Register
EECR	= '0x1f'

#:
GPIOR0	= '0x1e'

#:
EIMSK	= '0x1d'

#:
EIFR	= '0x1c'

#:
PCIFR	= '0x1b'

#:
TIFR2	= '0x17'

#:
TIFR1	= '0x16'

#:
TIFR0	= '0x15'

#:
PORTD	= '0x0b'

#:
DDRD	= '0x0a'

#:
PIND	= '0x09'

#:
PORTC	= '0x08'

#:
DDRC	= '0x07'

#:
PINC	= '0x06'

#:
PORTB	= '0x05'

#:
DDRB	= '0x04'

#:
PINB	= '0x03'


#########################################################################
#########################################################################
###
###   USART
###
#########################################################################
#########################################################################


#########################################################################
## UDR0 - USART I/O Data Register
#########################################################################

#: USART I/O Data Register bit 0
UDR0_0	= 0

#: USART I/O Data Register bit 1
UDR0_1	= 1

#: USART I/O Data Register bit 2
UDR0_2	= 2	

#: USART I/O Data Register bit 3
UDR0_3	= 3	

#: USART I/O Data Register bit 4
UDR0_4	= 4	

#: USART I/O Data Register bit 5
UDR0_5	= 5	

#: USART I/O Data Register bit 6
UDR0_6	= 6	

#: USART I/O Data Register bit 7
UDR0_7	= 7	


#########################################################################
## UCSR0A - USART Control and Status Register A
#########################################################################

#: UCSR0A - USART Control and Status Register A
#:
#: Multi-processor Communication Mode
MPCM0	= 0

#: UCSR0A - USART Control and Status Register A
#:
#: Double the USART transmission speed
U2X0	= 1

#: UCSR0A - USART Control and Status Register A
#:
#: Parity Error
UPE0	= 2

#: UCSR0A - USART Control and Status Register A
#:
#: Data overRun
DOR0	= 3

#: UCSR0A - USART Control and Status Register A
#:
#: Framing Error
FE0	= 4

#: UCSR0A - USART Control and Status Register A
#:
#: USART Data Register Empty
UDRE0	= 5

#: UCSR0A - USART Control and Status Register A
#:
#: USART Transmitt Complete
TXC0	= 6

#: UCSR0A - USART Control and Status Register A
#:
#: USART Receive Complete
RXC0	= 7


#########################################################################
## UCSR0B - USART Control and Status Register B
#########################################################################

#: UCSR0B - USART Control and Status Register B
#:
#: Transmit Data Bit 8
TXB80	= 0

#: UCSR0B - USART Control and Status Register B
#:
#: Receive Data Bit 8
RXB80	= 1

#: UCSR0B - USART Control and Status Register B
#:
#: Character Size
UCSZ02	= 2

#: UCSR0B - USART Control and Status Register B
#:
#: Transmitter Enable
TXEN0	= 3

#: UCSR0B - USART Control and Status Register B
#:
#: Receiver Enable
RXEN0	= 4

#: UCSR0B - USART Control and Status Register B
#:
#: USART Data register Empty Interrupt Enable
UDRIE0	= 5

#: UCSR0B - USART Control and Status Register B
#:
#: TX Complete Interrupt Enable
TXCIE0	= 6

#: UCSR0B - USART Control and Status Register B
#:
#: RX Complete Interrupt Enable
RXCIE0	= 7


#########################################################################
## UCSR0C - USART Control and Status Register C
#########################################################################

#: UCSR0C - USART Control and Status Register C
#:
#: Clock Polarity
UCPOL0	= 0

#: UCSR0C - USART Control and Status Register C
#:
#: Character Size
UCSZ00	= 1

#: UCSR0C - USART Control and Status Register C
#:
#: Character Size
UCSZ01	= 2

#: UCSR0C - USART Control and Status Register C
#:
#: Stop Bit Select
USBS0	= 3

#: UCSR0C - USART Control and Status Register C
#:
#: Parity Mode Bit 0
UPM00	= 4

#: UCSR0C - USART Control and Status Register C
#:
#: Parity Mode Bit 1
UPM01	= 5

#: UCSR0C - USART Control and Status Register C
#:
#: USART Mode Select
UMSEL00	= 6

#: UCSR0C - USART Control and Status Register C
#:
#: USART Mode Select
UMSEL01	= 7


#########################################################################
## USART Baud Rate Register 
#########################################################################

#: USART Baud Rate Register Low Byte bit 0
UBRR0	= 0

#: USART Baud Rate Register Low Byte bit 1
UBRR1	= 1

#: USART Baud Rate Register Low Byte bit 2
UBRR2	= 2

#: USART Baud Rate Register Low Byte bit 3
UBRR3	= 3

#: USART Baud Rate Register Low Byte bit 4
UBRR4	= 4

#: USART Baud Rate Register Low Byte bit 5
UBRR5	= 5

#: USART Baud Rate Register Low Byte bit 6
UBRR6	= 6

#: USART Baud Rate Register Low Byte bit 7
UBRR7	= 7

#: UBRR0H - USART Baud Rate Register High Byte bit 8
UBRR8	= 0

#: UBRR0H - USART Baud Rate Register High Byte bit 9
UBRR9	= 1

#: UBRR0H - USART Baud Rate Register High Byte bit 10
UBRR10	= 2

#: UBRR0H - USART Baud Rate Register High Byte bit 11
UBRR11	= 3


#########################################################################
#########################################################################
###
###   TWI
###
#########################################################################
#########################################################################


#########################################################################
## TWAMR - TWI Address Mask Register
#########################################################################

#: TWAMR - TWI Address Mask Register bit 0
TWAM0	= 1

#: TWAMR - TWI Address Mask Register bit 1
TWAM1	= 2

#: TWAMR - TWI Address Mask Register bit 2
TWAM2	= 3

#: TWAMR - TWI Address Mask Register bit 3
TWAM3	= 4

#: TWAMR - TWI Address Mask Register bit 4
TWAM4	= 5

#: TWAMR - TWI Address Mask Register bit 5
TWAM5	= 6

#: TWAMR - TWI Address Mask Register bit 6
TWAM6	= 7


#########################################################################
## TWBR - TWI Bit Rate register
#########################################################################

#: TWBR - TWI Bit Rate register bit 0
TWBR0	= 0

#: TWBR - TWI Bit Rate register bit 1
TWBR1	= 1

#: TWBR - TWI Bit Rate register bit 2
TWBR2	= 2

#: TWBR - TWI Bit Rate register bit 3
TWBR3	= 3

#: TWBR - TWI Bit Rate register bit 4
TWBR4	= 4

#: TWBR - TWI Bit Rate register bit 5
TWBR5	= 5

#: TWBR - TWI Bit Rate register bit 6
TWBR6	= 6

#: TWBR - TWI Bit Rate register bit 7
TWBR7	= 7


#########################################################################
## TWCR - TWI Control Register
#########################################################################

#: TWI Interrupt Enable
TWIE	= 0

#: TWI Enable Bit
TWEN	= 2

#: TWI Write Collition Flag
TWWC	= 3

#: TWI Stop Condition Bit
TWSTO	= 4

#: TWI Start Condition Bit
TWSTA	= 5

#: TWI Enable Acknowledge Bit
TWEA	= 6

#: TWI Interrupt Flag
TWINT	= 7


#########################################################################
# TWSR - TWI Status Register
#########################################################################

#: TWI Prescaler
TWPS0	= 0

#: TWI Prescaler
TWPS1	= 1

#: TWI Status
TWS3	= 3

#: TWI Status
TWS4	= 4

#: TWI Status
TWS5	= 5

#: TWI Status
TWS6	= 6

#: TWI Status
TWS7	= 7


#########################################################################
# TWDR - TWI Data register
#########################################################################

TWD0	= 0	#: TWI Data Register Bit 0
TWD1	= 1	#: TWI Data Register Bit 1
TWD2	= 2	#: TWI Data Register Bit 2
TWD3	= 3	#: TWI Data Register Bit 3
TWD4	= 4	#: TWI Data Register Bit 4
TWD5	= 5	#: TWI Data Register Bit 5
TWD6	= 6	#: TWI Data Register Bit 6
TWD7	= 7	#: TWI Data Register Bit 7

# TWAR - TWI (Slave) Address register
TWGCE	= 0	#: TWI General Call Recognition Enable Bit
TWA0	= 1	#: TWI (Slave) Address register Bit 0
TWA1	= 2	#: TWI (Slave) Address register Bit 1
TWA2	= 3	#: TWI (Slave) Address register Bit 2
TWA3	= 4	#: TWI (Slave) Address register Bit 3
TWA4	= 5	#: TWI (Slave) Address register Bit 4
TWA5	= 6	#: TWI (Slave) Address register Bit 5
TWA6	= 7	#: TWI (Slave) Address register Bit 6


# ***** TIMER_COUNTER_1 **************
# TIMSK1 - Timer/Counter Interrupt Mask Register
TOIE1	= 0	#: Timer/Counter1 Overflow Interrupt Enable
OCIE1A	= 1	#: Timer/Counter1 Output CompareA Match Interrupt Enable
OCIE1B	= 2	#: Timer/Counter1 Output CompareB Match Interrupt Enable
ICIE1	= 5	#: Timer/Counter1 Input Capture Interrupt Enable

# TIFR1 - Timer/Counter Interrupt Flag register
TOV1	= 0	#: Timer/Counter1 Overflow Flag
OCF1A	= 1	#: Output Compare Flag 1A
OCF1B	= 2	#: Output Compare Flag 1B
ICF1	= 5	#: Input Capture Flag 1

# TCCR1A - Timer/Counter1 Control Register A
WGM10	= 0	#: Waveform Generation Mode
WGM11	= 1	#: Waveform Generation Mode
COM1B0	= 4	#: Compare Output Mode 1B, bit 0
COM1B1	= 5	#: Compare Output Mode 1B, bit 1
COM1A0	= 6	#: Comparet Ouput Mode 1A, bit 0
COM1A1	= 7	#: Compare Output Mode 1A, bit 1

# TCCR1B - Timer/Counter1 Control Register B
CS10	= 0	#: Prescaler source of Timer/Counter 1
CS11	= 1	#: Prescaler source of Timer/Counter 1
CS12	= 2	#: Prescaler source of Timer/Counter 1
WGM12	= 3	#: Waveform Generation Mode
WGM13	= 4	#: Waveform Generation Mode
ICES1	= 6	#: Input Capture 1 Edge Select
ICNC1	= 7	#: Input Capture 1 Noise Canceler

# TCCR1C - Timer/Counter1 Control Register C
FOC1B	= 6	#: TCCR1C - Timer/Counter1 Control Register C
FOC1A	= 7	#: TCCR1C - Timer/Counter1 Control Register C

# GTCCR - General Timer/Counter Control Register
PSRSYNC	= 0	#: Prescaler Reset Timer/Counter1 and Timer/Counter0
TSM	= 7	#: Timer/Counter Synchronization Mode


# ***** TIMER_COUNTER_2 **************
# TIMSK2 - Timer/Counter Interrupt Mask register
TOIE2	= 0	#: Timer/Counter2 Overflow Interrupt Enable
##TOIE2A	= TOIE2	# For compatibility
OCIE2A	= 1	#: Timer/Counter2 Output Compare Match A Interrupt Enable
OCIE2B	= 2	#: Timer/Counter2 Output Compare Match B Interrupt Enable

# TIFR2 - Timer/Counter Interrupt Flag Register
TOV2	= 0	#: Timer/Counter2 Overflow Flag
OCF2A	= 1	#: Output Compare Flag 2A
OCF2B	= 2	#: Output Compare Flag 2B

# TCCR2A - Timer/Counter2 Control Register A
WGM20	= 0	#: Waveform Genration Mode
WGM21	= 1	#: Waveform Genration Mode
COM2B0	= 4	#: Compare Output Mode bit 0
COM2B1	= 5	#: Compare Output Mode bit 1
COM2A0	= 6	#: Compare Output Mode bit 1
COM2A1	= 7	#: Compare Output Mode bit 1

# TCCR2B - Timer/Counter2 Control Register B
CS20	= 0	#: Clock Select bit 0
CS21	= 1	#: Clock Select bit 1
CS22	= 2	#: Clock Select bit 2
WGM22	= 3	#: Waveform Generation Mode
FOC2B	= 6	#: Force Output Compare B
FOC2A	= 7	#: Force Output Compare A

# TCNT2 - Timer/Counter2
TCNT2_0	= 0	#: Timer/Counter 2 bit 0
TCNT2_1	= 1	#: Timer/Counter 2 bit 1
TCNT2_2	= 2	#: Timer/Counter 2 bit 2
TCNT2_3	= 3	#: Timer/Counter 2 bit 3
TCNT2_4	= 4	#: Timer/Counter 2 bit 4
TCNT2_5	= 5	#: Timer/Counter 2 bit 5
TCNT2_6	= 6	#: Timer/Counter 2 bit 6
TCNT2_7	= 7	#: Timer/Counter 2 bit 7

# OCR2A - Timer/Counter2 Output Compare Register A
OCR2A_0	= 0	#: Timer/Counter2 Output Compare Register Bit 0
OCR2A_1	= 1	#: Timer/Counter2 Output Compare Register Bit 1
OCR2A_2	= 2	#: Timer/Counter2 Output Compare Register Bit 2
OCR2A_3	= 3	#: Timer/Counter2 Output Compare Register Bit 3
OCR2A_4	= 4	#: Timer/Counter2 Output Compare Register Bit 4
OCR2A_5	= 5	#: Timer/Counter2 Output Compare Register Bit 5
OCR2A_6	= 6	#: Timer/Counter2 Output Compare Register Bit 6
OCR2A_7	= 7	#: Timer/Counter2 Output Compare Register Bit 7

# OCR2B - Timer/Counter2 Output Compare Register B
OCR2B_0	= 0	#: Timer/Counter2 Output Compare Register Bit 0
OCR2B_1	= 1	#: Timer/Counter2 Output Compare Register Bit 1
OCR2B_2	= 2	#: Timer/Counter2 Output Compare Register Bit 2
OCR2B_3	= 3	#: Timer/Counter2 Output Compare Register Bit 3
OCR2B_4	= 4	#: Timer/Counter2 Output Compare Register Bit 4
OCR2B_5	= 5	#: Timer/Counter2 Output Compare Register Bit 5
OCR2B_6	= 6	#: Timer/Counter2 Output Compare Register Bit 6
OCR2B_7	= 7	#: Timer/Counter2 Output Compare Register Bit 7

# ASSR - Asynchronous Status Register
TCR2BUB	= 0	#: Timer/Counter Control Register2 Update Busy
TCR2AUB	= 1	#: Timer/Counter Control Register2 Update Busy
OCR2BUB	= 2	#: Output Compare Register 2 Update Busy
OCR2AUB	= 3	#: Output Compare Register2 Update Busy
TCN2UB	= 4	#: Timer/Counter2 Update Busy
AS2	= 5	#: Asynchronous Timer/Counter2
EXCLK	= 6	#: Enable External Clock Input

# GTCCR - General Timer Counter Control register
PSRASY	= 1	# :Prescaler Reset Timer/Counter2
##PSR2	= PSRASY	# For compatibility
TSM	= 7	#: Timer/Counter Synchronization Mode



# ***** AD_CONVERTER *****************
# ADMUX - The ADC multiplexer Selection Register
MUX0	= 0	#: Analog Channel and Gain Selection Bits
MUX1	= 1	#: Analog Channel and Gain Selection Bits
MUX2	= 2	#: Analog Channel and Gain Selection Bits
MUX3	= 3	#: Analog Channel and Gain Selection Bits
ADLAR	= 5	#: Left Adjust Result
REFS0	= 6	#: Reference Selection Bit 0
REFS1	= 7	#: Reference Selection Bit 1

# ADCSRA - The ADC Control and Status register A
ADPS0	= 0	#: ADC  Prescaler Select Bits
ADPS1	= 1	#: ADC  Prescaler Select Bits
ADPS2	= 2	#: ADC  Prescaler Select Bits
ADIE	= 3	#: ADC Interrupt Enable
ADIF	= 4	#: ADC Interrupt Flag
ADATE	= 5	#: ADC  Auto Trigger Enable
ADSC	= 6	#: ADC Start Conversion
ADEN	= 7	#: ADC Enable

# ADCSRB - The ADC Control and Status register B
ADTS0	= 0	#: ADC Auto Trigger Source bit 0
ADTS1	= 1	#: ADC Auto Trigger Source bit 1
ADTS2	= 2	#: ADC Auto Trigger Source bit 2
ACME	= 6	# 

# ADCH - ADC Data Register High Byte
ADCH0	= 0	#: ADC Data Register High Byte Bit 0
ADCH1	= 1	#: ADC Data Register High Byte Bit 1
ADCH2	= 2	#: ADC Data Register High Byte Bit 2
ADCH3	= 3	#: ADC Data Register High Byte Bit 3
ADCH4	= 4	#: ADC Data Register High Byte Bit 4
ADCH5	= 5	#: ADC Data Register High Byte Bit 5
ADCH6	= 6	#: ADC Data Register High Byte Bit 6
ADCH7	= 7	#: ADC Data Register High Byte Bit 7

# ADCL - ADC Data Register Low Byte
ADCL0	= 0	#: ADC Data Register Low Byte Bit 0
ADCL1	= 1	#: ADC Data Register Low Byte Bit 1
ADCL2	= 2	#: ADC Data Register Low Byte Bit 2
ADCL3	= 3	#: ADC Data Register Low Byte Bit 3
ADCL4	= 4	#: ADC Data Register Low Byte Bit 4
ADCL5	= 5	#: ADC Data Register Low Byte Bit 5
ADCL6	= 6	#: ADC Data Register Low Byte Bit 6
ADCL7	= 7	#: ADC Data Register Low Byte Bit 7

# DIDR0 - Digital Input Disable Register
ADC0D	= 0	#: Digital Input Disable Bit 0
ADC1D	= 1	#: Digital Input Disable Bit 1
ADC2D	= 2	#: Digital Input Disable Bit 2
ADC3D	= 3	#: Digital Input Disable Bit 3
ADC4D	= 4	#: Digital Input Disable Bit 4
ADC5D	= 5	#: Digital Input Disable Bit 5


# ***** ANALOG_COMPARATOR ************
# ACSR - Analog Comparator Control And Status Register
ACIS0	= 0	#: Analog Comparator Interrupt Mode Select bit 0
ACIS1	= 1	#: Analog Comparator Interrupt Mode Select bit 1
ACIC	= 2	#: Analog Comparator Input Capture Enable
ACIE	= 3	#: Analog Comparator Interrupt Enable
ACI	= 4	#: Analog Comparator Interrupt Flag
ACO	= 5	#: Analog Compare Output
ACBG	= 6	#: Analog Comparator Bandgap Select
ACD	= 7	#: Analog Comparator Disable

# DIDR1 - Digital Input Disable Register 1
AIN0D	= 0	#: AIN0 Digital Input Disable
AIN1D	= 1	#: AIN1 Digital Input Disable


# ***** PORTB ************************
# PORTB - Port B Data Register
PORTB0	= 0	#: Port B Data Register bit 0
PB0	= 0	#: Port B Data Register bit 0
PORTB1	= 1	#: Port B Data Register bit 1
PB1	= 1	#: Port B Data Register bit 1
PORTB2	= 2	#: Port B Data Register bit 2
PB2	= 2	#: Port B Data Register bit 2
PORTB3	= 3	#: Port B Data Register bit 3
PB3	= 3	#: Port B Data Register bit 3
PORTB4	= 4	#: Port B Data Register bit 4
PB4	= 4	#: Port B Data Register bit 4
PORTB5	= 5	#: Port B Data Register bit 5
PB5	= 5	#: Port B Data Register bit 5
PORTB6	= 6	#: Port B Data Register bit 6
PB6	= 6	#: Port B Data Register bit 6
PORTB7	= 7	#: Port B Data Register bit 7
PB7	= 7	#: Port B Data Register bit 7

# DDRB - Port B Data Direction Register
DDB0	= 0	#: Port B Data Direction Register bit 0
DDB1	= 1	#: Port B Data Direction Register bit 1
DDB2	= 2	#: Port B Data Direction Register bit 2
DDB3	= 3	#: Port B Data Direction Register bit 3
DDB4	= 4	#: Port B Data Direction Register bit 4
DDB5	= 5	#: Port B Data Direction Register bit 5
DDB6	= 6	#: Port B Data Direction Register bit 6
DDB7	= 7	#: Port B Data Direction Register bit 7

# PINB - Port B Input Pins
PINB0	= 0	#: Port B Input Pins bit 0
PINB1	= 1	#: Port B Input Pins bit 1
PINB2	= 2	#: Port B Input Pins bit 2
PINB3	= 3	#: Port B Input Pins bit 3
PINB4	= 4	#: Port B Input Pins bit 4
PINB5	= 5	#: Port B Input Pins bit 5
PINB6	= 6	#: Port B Input Pins bit 6
PINB7	= 7	#: Port B Input Pins bit 7


# ***** PORTC ************************
# PORTC - Port C Data Register
PORTC0	= 0	#: Port C Data Register bit 0
PC0	= 0	# For compatibility
PORTC1	= 1	#: Port C Data Register bit 1
PC1	= 1	# For compatibility
PORTC2	= 2	#: Port C Data Register bit 2
PC2	= 2	# For compatibility
PORTC3	= 3	#: Port C Data Register bit 3
PC3	= 3	# For compatibility
PORTC4	= 4	#: Port C Data Register bit 4
PC4	= 4	# For compatibility
PORTC5	= 5	#: Port C Data Register bit 5
PC5	= 5	# For compatibility
PORTC6	= 6	#: Port C Data Register bit 6
PC6	= 6	# For compatibility

# DDRC - Port C Data Direction Register
DDC0	= 0	#: Port C Data Direction Register bit 0
DDC1	= 1	#: Port C Data Direction Register bit 1
DDC2	= 2	#: Port C Data Direction Register bit 2
DDC3	= 3	#: Port C Data Direction Register bit 3
DDC4	= 4	#: Port C Data Direction Register bit 4
DDC5	= 5	#: Port C Data Direction Register bit 5
DDC6	= 6	#: Port C Data Direction Register bit 6

# PINC - Port C Input Pins
PINC0	= 0	#: Port C Input Pins bit 0
PINC1	= 1	#: Port C Input Pins bit 1
PINC2	= 2	#: Port C Input Pins bit 2
PINC3	= 3	#: Port C Input Pins bit 3
PINC4	= 4	#: Port C Input Pins bit 4
PINC5	= 5	#: Port C Input Pins bit 5
PINC6	= 6	#: Port C Input Pins bit 6


# ***** PORTD ************************
# PORTD - Port D Data Register
PORTD0	= 0	#: Port D Data Register bit 0
PD0	= 0	# For compatibility
PORTD1	= 1	#: Port D Data Register bit 1
PD1	= 1	# For compatibility
PORTD2	= 2	#: Port D Data Register bit 2
PD2	= 2	# For compatibility
PORTD3	= 3	#: Port D Data Register bit 3
PD3	= 3	# For compatibility
PORTD4	= 4	#: Port D Data Register bit 4
PD4	= 4	# For compatibility
PORTD5	= 5	#: Port D Data Register bit 5
PD5	= 5	# For compatibility
PORTD6	= 6	#: Port D Data Register bit 6
PD6	= 6	# For compatibility
PORTD7	= 7	#: Port D Data Register bit 7
PD7	= 7	# For compatibility

# DDRD - Port D Data Direction Register
DDD0	= 0	#: Port D Data Direction Register bit 0
DDD1	= 1	#: Port D Data Direction Register bit 1
DDD2	= 2	#: Port D Data Direction Register bit 2
DDD3	= 3	#: Port D Data Direction Register bit 3
DDD4	= 4	#: Port D Data Direction Register bit 4
DDD5	= 5	#: Port D Data Direction Register bit 5
DDD6	= 6	#: Port D Data Direction Register bit 6
DDD7	= 7	#: Port D Data Direction Register bit 7

# PIND - Port D Input Pins
PIND0	= 0	#: Port D Input Pins bit 0
PIND1	= 1	#: Port D Input Pins bit 1
PIND2	= 2	#: Port D Input Pins bit 2
PIND3	= 3	#: Port D Input Pins bit 3
PIND4	= 4	#: Port D Input Pins bit 4
PIND5	= 5	#: Port D Input Pins bit 5
PIND6	= 6	#: Port D Input Pins bit 6
PIND7	= 7	#: Port D Input Pins bit 7


# ***** TIMER_COUNTER_0 **************
# TIMSK0 - Timer/Counter0 Interrupt Mask Register
TOIE0	= 0	#: Timer/Counter0 Overflow Interrupt Enable
OCIE0A	= 1	#: Timer/Counter0 Output Compare Match A Interrupt Enable
OCIE0B	= 2	#: Timer/Counter0 Output Compare Match B Interrupt Enable

# TIFR0 - Timer/Counter0 Interrupt Flag register
TOV0	= 0	#: Timer/Counter0 Overflow Flag
OCF0A	= 1	#: Timer/Counter0 Output Compare Flag 0A
OCF0B	= 2	#: Timer/Counter0 Output Compare Flag 0B

# TCCR0A - Timer/Counter  Control Register A
WGM00	= 0	#: Waveform Generation Mode
WGM01	= 1	#: Waveform Generation Mode
COM0B0	= 4	#: Compare Output Mode, Fast PWm
COM0B1	= 5	#: Compare Output Mode, Fast PWm
COM0A0	= 6	#: Compare Output Mode, Phase Correct PWM Mode
COM0A1	= 7	#: Compare Output Mode, Phase Correct PWM Mode

# TCCR0B - Timer/Counter Control Register B
CS00	= 0	#: Clock Select
CS01	= 1	#: Clock Select
CS02	= 2	#: Clock Select
WGM02	= 3	#:
FOC0B	= 6	#: Force Output Compare B
FOC0A	= 7	#: Force Output Compare A

# TCNT0 - Timer/Counter0
TCNT0_0	= 0	#:
TCNT0_1	= 1	#: 
TCNT0_2	= 2	#: 
TCNT0_3	= 3	#: 
TCNT0_4	= 4	#: 
TCNT0_5	= 5	#: 
TCNT0_6	= 6	#: 
TCNT0_7	= 7	#: 

# OCR0A - Timer/Counter0 Output Compare Register
OCR0A_0	= 0	#: 
OCR0A_1	= 1	#: 
OCR0A_2	= 2	#: 
OCR0A_3	= 3	#: 
OCR0A_4	= 4	#: 
OCR0A_5	= 5	#: 
OCR0A_6	= 6	#: 
OCR0A_7	= 7	#: 

# OCR0B - Timer/Counter0 Output Compare Register
OCR0B_0	= 0	#: 
OCR0B_1	= 1	#: 
OCR0B_2	= 2	#: 
OCR0B_3	= 3	#: 
OCR0B_4	= 4	#: 
OCR0B_5	= 5	#: 
OCR0B_6	= 6	#: 
OCR0B_7	= 7	#: 

# GTCCR - General Timer/Counter Control Register
#PSRSYNC	= 0	#: Prescaler Reset Timer/Counter1 and Timer/Counter0
PSR10	= 0	#: For compatibility
#TSM	= 7	#: Timer/Counter Synchronization Mode


# ***** EXTERNAL_INTERRUPT ***********
# EICRA - External Interrupt Control Register
ISC00	= 0	#: External Interrupt Sense Control 0 Bit 0
ISC01	= 1	#: External Interrupt Sense Control 0 Bit 1
ISC10	= 2	#: External Interrupt Sense Control 1 Bit 0
ISC11	= 3	#: External Interrupt Sense Control 1 Bit 1

# EIMSK - External Interrupt Mask Register
INT0	= 0	#: External Interrupt Request 0 Enable
INT1	= 1	#: External Interrupt Request 1 Enable

# EIFR - External Interrupt Flag Register
INTF0	= 0	#: External Interrupt Flag 0
INTF1	= 1	#: External Interrupt Flag 1

# PCICR - Pin Change Interrupt Control Register
PCIE0	= 0	#: Pin Change Interrupt Enable 0
PCIE1	= 1	#: Pin Change Interrupt Enable 1
PCIE2	= 2	#: Pin Change Interrupt Enable 2

# PCMSK2 - Pin Change Mask Register 2
PCINT16	= 0	#: Pin Change Enable Mask 16
PCINT17	= 1	#: Pin Change Enable Mask 17
PCINT18	= 2	#: Pin Change Enable Mask 18
PCINT19	= 3	#: Pin Change Enable Mask 19
PCINT20	= 4	#: Pin Change Enable Mask 20
PCINT21	= 5	#: Pin Change Enable Mask 21
PCINT22	= 6	#: Pin Change Enable Mask 22
PCINT23	= 7	#: Pin Change Enable Mask 23

# PCMSK1 - Pin Change Mask Register 1
PCINT8	= 0	#: Pin Change Enable Mask 8
PCINT9	= 1	#: Pin Change Enable Mask 9
PCINT10	= 2	#: Pin Change Enable Mask 10
PCINT11	= 3	#: Pin Change Enable Mask 11
PCINT12	= 4	#: Pin Change Enable Mask 12
PCINT13	= 5	#: Pin Change Enable Mask 13
PCINT14	= 6	#: Pin Change Enable Mask 14

# PCMSK0 - Pin Change Mask Register 0
PCINT0	= 0	#: Pin Change Enable Mask 0
PCINT1	= 1	#: Pin Change Enable Mask 1
PCINT2	= 2	#: Pin Change Enable Mask 2
PCINT3	= 3	#: Pin Change Enable Mask 3
PCINT4	= 4	#: Pin Change Enable Mask 4
PCINT5	= 5	#: Pin Change Enable Mask 5
PCINT6	= 6	#: Pin Change Enable Mask 6
PCINT7	= 7	#: Pin Change Enable Mask 7

# PCIFR - Pin Change Interrupt Flag Register
PCIF0	= 0	#: Pin Change Interrupt Flag 0
PCIF1	= 1	#: Pin Change Interrupt Flag 1
PCIF2	= 2	#: Pin Change Interrupt Flag 2


# ***** SPI **************************
# SPDR - SPI Data Register
SPDR0	= 0	#: SPI Data Register bit 0
SPDR1	= 1	#: SPI Data Register bit 1
SPDR2	= 2	#: SPI Data Register bit 2
SPDR3	= 3	#: SPI Data Register bit 3
SPDR4	= 4	#: SPI Data Register bit 4
SPDR5	= 5	#: SPI Data Register bit 5
SPDR6	= 6	#: SPI Data Register bit 6
SPDR7	= 7	#: SPI Data Register bit 7

# SPSR - SPI Status Register
SPI2X	= 0	#: Double SPI Speed Bit
WCOL	= 6	#: Write Collision Flag
SPIF	= 7	#: SPI Interrupt Flag

# SPCR - SPI Control Register
SPR0	= 0	#: SPI Clock Rate Select 0
SPR1	= 1	#: SPI Clock Rate Select 1
CPHA	= 2	#: Clock Phase
CPOL	= 3	#: Clock polarity
MSTR	= 4	#: Master/Slave Select
DORD	= 5	#: Data Order
SPE	= 6	#: SPI Enable
SPIE	= 7	#: SPI Interrupt Enable


# ***** WATCHDOG *********************
# WDTCSR - Watchdog Timer Control Register
WDP0	= 0	#: Watch Dog Timer Prescaler bit 0
WDP1	= 1	#: Watch Dog Timer Prescaler bit 1
WDP2	= 2	#: Watch Dog Timer Prescaler bit 2
WDE	= 3	#: Watch Dog Enable
WDCE	= 4	#: Watchdog Change Enable
WDP3	= 5	#: Watchdog Timer Prescaler Bit 3
WDIE	= 6	#: Watchdog Timeout Interrupt Enable
WDIF	= 7	#: Watchdog Timeout Interrupt Flag


# ***** CPU **************************
# SREG - Status Register

#: Carry Flag
SREG_C	= 0

#: Zero Flag
SREG_Z	= 1

#: Negative Flag
SREG_N	= 2

#: Two's Complement Overflow Flag
SREG_V	= 3

#: Sign Bit
SREG_S	= 4

#: Half Carry Flag
SREG_H	= 5

#: Bit Copy Storage
SREG_T	= 6

#: Global Interrupt Enable
SREG_I	= 7


# CLKPR - Clock Prescale Register
CLKPS0	= 0	#: Clock Prescaler Select Bit 0
CLKPS1	= 1	#: Clock Prescaler Select Bit 1
CLKPS2	= 2	#: Clock Prescaler Select Bit 2
CLKPS3	= 3	#: Clock Prescaler Select Bit 3
CLKPCE	= 7	#: Clock Prescaler Change Enable


# MCUCR - MCU Control Register
IVCE	= 0	#: 
IVSEL	= 1	#: 
PUD	= 4	#: 
BODSE	= 5	#: BOD Sleep Enable
BODS	= 6	#: BOD Sleep

# MCUSR - MCU Status Register
PORF	= 0	#: Power-on reset flag
EXTRF	= 1	#: External Reset Flag
EXTREF	= 1	#: For compatibility
BORF	= 2	#: Brown-out Reset Flag
WDRF	= 3	#: Watchdog Reset Flag

# SMCR - Sleep Mode Control Register
SE	= 0	#: Sleep Enable
SM0	= 1	#: Sleep Mode Select Bit 0
SM1	= 2	#: Sleep Mode Select Bit 1
SM2	= 3	#: Sleep Mode Select Bit 2

# GPIOR2 - General Purpose I/O Register 2
GPIOR20	= 0	#: 
GPIOR21	= 1	#: 
GPIOR22	= 2	#: 
GPIOR23	= 3	#: 
GPIOR24	= 4	#: 
GPIOR25	= 5	#: 
GPIOR26	= 6	#: 
GPIOR27	= 7	#: 

# GPIOR1 - General Purpose I/O Register 1
GPIOR10	= 0	#: 
GPIOR11	= 1	#: 
GPIOR12	= 2	#: 
GPIOR13	= 3	#: 
GPIOR14	= 4	#: 
GPIOR15	= 5	#: 
GPIOR16	= 6	#: 
GPIOR17	= 7	#: 

# GPIOR0 - General Purpose I/O Register 0
GPIOR00	= 0	#: 
GPIOR01	= 1	#: 
GPIOR02	= 2	#: 
GPIOR03	= 3	#: 
GPIOR04	= 4	#: 
GPIOR05	= 5	#: 
GPIOR06	= 6	#: 
GPIOR07	= 7	#: 

# PRR - Power Reduction Register
PRADC	= 0	#: Power Reduction ADC
PRUSART0	= 1	#: Power Reduction USART
PRSPI	= 2	#: Power Reduction Serial Peripheral Interface
PRTIM1	= 3	#: Power Reduction Timer/Counter1
PRTIM0	= 5	#: Power Reduction Timer/Counter0
PRTIM2	= 6	#: Power Reduction Timer/Counter2
PRTWI	= 7	#: Power Reduction TWI


# ***** DATA MEMORY DECLARATIONS *****************************************
FLASHEND	= 0x3fff #:
IOEND	= 0x00ff #:
SRAM_START	= 0x0100 #:
SRAM_SIZE	= 2048 #:
RAMEND	= 0x08ff #:
XRAMEND	= 0x0000 #:
E2END	= 0x03ff #:
EEPROMEND	= 0x03ff #:
EEADRBITS	= 10 #:


#########################################################################
## Register mnemonics.
#########################################################################

r0 = 0 #: Register 0
r1 = 1 #: Register 1
r2 = 2 #: Register 2
r3 = 3 #: Register 3
r4 = 4 #: Register 4
r5 = 5 #: Register 5
r6 = 6 #: Register 6
r7 = 7 #: Register 7
r8 = 8 #: Register 8
r9 = 9 #: Register 9
r10 = 10 #: Register 10
r11 = 11 #: Register 11
r12 = 12 #: Register 12
r13 = 13 #: Register 13
r14 = 14 #: Register 14
r15 = 15 #: Register 15
r16 = 16 #: Register 16
r17 = 17 #: Register 17
r18 = 18 #: Register 18
r19 = 19 #: Register 19
r20 = 20 #: Register 20
r21 = 21 #: Register 21
r22 = 22 #: Register 22
r23 = 23 #: Register 23
r24 = 24 #: Register 24
r25 = 25 #: Register 25
r26 = 26 #: Register 26
r27 = 27 #: Register 27
r28 = 28 #: Register 28
r29 = 29 #: Register 29
r30 = 30 #: Register 30
r31 = 31 #: Register 31


X = r26 #:
XL = r26 #:
XH = r27 #:

Y = r28 #:
YL = r28 #:
YH = r29 #:

Z = r30 #:
ZL = r30 #:
ZH = r31 #:


UCPHA0	= UCSZ00	# For compatibility
UDORD0	= UCSZ01	# For compatibility
UMSEL0	= UMSEL00	# For compatibility
UMSEL1	= UMSEL01	# For compatibility
TWAMR0	= TWAM0	# For compatibility
TWAMR1	= TWAM1	# For compatibility
TWAMR2	= TWAM2	# For compatibility
TWAMR3	= TWAM3	# For compatibility
TWAMR4	= TWAM4	# For compatibility
TWAMR5	= TWAM5	# For compatibility
TWAMR6	= TWAM6	# For compatibility


defs = set(dir()) - _mark
defs.remove('_mark')
defs = dict(
  (k, _f(v))
  for k, v in locals().iteritems()
  if k in defs
  )


if __name__ == '__main__':
  import pprint
  pprint.pprint(defs)
