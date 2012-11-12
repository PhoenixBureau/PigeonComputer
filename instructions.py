from util import A, B, B_reversed, C, D, E, F, G, H, instr, spec, spec_reversed


_mark = set(dir()) ; _mark.add('_mark')


@A
def jmp(address):
  '''
  1001 010k kkkk 110k
  kkkk kkkk kkkk kkkk
  '''


def cli():
  return 16, 0b1001010011111000


@B
def ldi(register, immediate):
  '''
  1110 KKKK dddd KKKK
  '''


@C
def out(io_port, register):
  '''
  1011 1AAr rrrr AAAA
  '''


@A
def rcall(address):
  '''
  1101 kkkk kkkk kkkk
  '''


@B_reversed
def sts(address, register):
  '''
  1001 001d dddd 0000
  kkkk kkkk kkkk kkkk
  '''


@D
def mov(Rd, Rr):
  '''
  0010 11rd dddd rrrr
  '''


def sei():
  return 16, 0b1001010001111000


def ret():
  return 16, 0b1001010100001000


@A
def rjmp(address):
  '''
  1100 kkkk kkkk kkkk
  '''


@B
def lds(register, address):
  '''
  1001 000d dddd 0000
  kkkk kkkk kkkk kkkk
  '''


@E
def sbrs(register, bit):
  '''
  1111 111r rrrr 0bbb
  '''


def dw(values, data):
  return -1, data


def db(values, data):
  return -1, data


@F
def st_post_incr_Y(Rr):
  '''
  1001 001r rrrr 1001
  '''


@F
def st_post_incr_Z(Rr):
  '''
  1001 001r rrrr 0001
  '''


@G
def ld_pre_decr_Y(Rd):
  '''
  1001 000d dddd 1010
  '''


@G
def ld_post_incr_X(Rd):
  '''
  1001 000d dddd 1101
  '''


@G
def ld_post_incr_Z(Rd):
  '''
  1001 000d dddd 0001
  '''


@G
def ld_pre_decr_Z(Rd):
  '''
  1001 000d dddd 0010
  '''


@G
def lpm(Rd):
  '''
  1001 000d dddd 0100
  '''


@G
def lpm_post_incr_Z(Rd):
  '''
  1001 000d dddd 0101
  '''


@B
def cpi(register, immediate):
  '''
  0011 KKKK dddd KKKK
  '''


@A
def brne(address):
  '''
  1111 01kk kkkk k001
  '''


@A
def breq(address):
  '''
  1111 00kk kkkk k001
  '''


@A
def brlo(address):
  '''
  1111 00kk kkkk k000
  '''


@G
def lsr(Rd):
  '''
  1001 010d dddd 0110
  '''


@G
def lsl(Rd):
  '''
  0000 11dd dddd dddd
  '''


@D
def add(Rd, Rr):
  '''
  0000 11rd dddd rrrr
  '''


@A
def brcc(address):
  '''
  1111 01kk kkkk k000
  '''


@G
def inc(Rd):
  '''
  1001 010d dddd 0011
  '''


@G
def dec(Rd):
  '''
  1001 010d dddd 1010
  '''


def ijmp():
  return 16, 0b1001010000001001


@D
def cp(Rd, Rr):
  '''
  0001 01rd dddd rrrr
  '''


@D
def cpse(Rd, Rr):
  '''
  0001 00rd dddd rrrr
  '''


@D
def cpc(Rd, Rr):
  '''
  0000 01rd dddd rrrr
  '''


@A
def brsh(address):
  '''
  1111 01kk kkkk k000
  '''


@D
def movw(Rd, Rr):
  '''
  0000 0001 dddd rrrr
  '''


@B
def andi(register, immediate):
  '''
  0111 KKKK dddd KKKK
  '''


@H
def sbis(register, bit):
  '''
  1001 1011 AAAA Abbb
  '''


@G
def clr(Rd):
  '''
  0010 01dd dddd dddd
  '''


@F
def push(Rr):
  '''
  1001 001r rrrr 1111
  '''


@G
def pop(Rd):
  '''
  1001 000d dddd 1111
  '''


@D
def or_(Rd, Rr):
  '''
  0010 10rd dddd rrrr
  '''


@G
def swap(Rd):
  '''
  1001 010d dddd 0010
  '''


@B
def adiw(register, immediate):
  '''
  1001 0110 KKdd KKKK
  '''


@B
def sbiw(register, immediate):
  '''
  1001 0111 KKdd KKKK
  '''


@B
def subi(register, immediate):
  '''
  0101 KKKK dddd KKKK
  '''


@D
def mul(Rd, Rr):
  '''
  1001 11rd dddd rrrr
  '''


ops = dict(
  (name, func)
  for name, func in locals().iteritems()
  if name not in _mark
  )


class InstructionsMixin(object):

  @instr
  def jmp(self, address):
    self.here += 2
    return address

  @instr
  def rjmp(self, address):
    return address

  @instr
  def rcall(self, address):
    return address

  @instr
  def cli(self):
    pass

  @instr
  def sei(self):
    pass

  @instr
  def ret(self):
    pass

  @instr
  def ldi(self, target, address):
    if isinstance(address, str):
      assert len(address) == 1, repr(address)
      address = ord(address)
    return target, address << 1

  @instr
  def out(self, target, address):
    return target, address

  @instr
  def sts(self, address, register):
    self.here += 2
    return address << 1, register

  @instr
  def mov(self, target, source):
    return target, source

  @instr
  def lds(self, target, address):
    self.here += 2
    return target, address << 1

  @instr
  def sbrs(self, target, address):
    return target, address

  @spec
  def st_post_incr(self, ptr, register):
    pass

  @spec_reversed
  def ld_post_incr(self, register, ptr):
    pass

  @spec_reversed
  def ld_pre_decr(self, register, ptr):
    pass

  @spec_reversed
  def lpm_post_incr(self, register, ptr):
    pass

  @instr
  def cpi(self, register, immediate):
    if isinstance(immediate, str):
      assert len(immediate) == 1, repr(immediate)
      immediate = ord(immediate)
    return register, immediate << 1

  @instr
  def brne(self, address):
    return address

  @instr
  def breq(self, address):
    return address

  @instr
  def inc(self, address):
    return address

  @instr
  def mul(self, target, source):
    return target, source

  @instr
  def brlo(self, address):
    return address

  @instr
  def subi(self, target, source):
    return target, source

  @instr
  def add(self, target, source):
    return target, source

  @instr
  def dec(self, address):
    return address

  @instr
  def clr(self, address):
    return address

  @instr
  def lsl(self, address):
    return address

  @instr
  def brcc(self, address):
    return address

  @instr
  def or_(self, target, source):
    return target, source

  @instr
  def push(self, address):
    return address

  @instr
  def swap(self, address):
    return address

  @instr
  def pop(self, address):
    return address

  @instr
  def movw(self, target, source):
    return target, source

  @instr
  def andi(self, target, source):
    return target, source

  @instr
  def adiw(self, target, source):
    return target, source

  def lpm(self, target, source):
    assert source == 30, repr(source) # Must be Z
    self._one('lpm', target)

  @instr
  def cp(self, target, source):
    return target, source

  @instr
  def cpc(self, target, source):
    return target, source

  @instr
  def brsh(self, address):
    return address

  @instr
  def cpse(self, target, source):
    return target, source

  @instr
  def sbiw(self, target, source):
    return target, source

  @instr
  def lsr(self, address):
    return address

  @instr
  def ijmp(self):
    pass

  def _one(self, op, address):
    name, address = self._name_or_addr(address)
    addr = self._get_here()
    print 'assembling %s instruction at %s to %s' % (op, addr, name)
    self.data[addr] = (op, address)
    self.here += 2

  def _instruction_namespace(self):
    for n in dir(InstructionsMixin):
      if n.startswith('_'):
        continue
      yield n, getattr(self, n)


if __name__ == '__main__':
  import pprint
  pprint.pprint(ops)
  pprint.pprint(dict(InstructionsMixin()._instruction_namespace()))
