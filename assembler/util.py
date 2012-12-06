from struct import pack
from functools import wraps
from myhdl import intbv, concat


ADDRESS_MAX = 0x3fff


def update(a, b):
  '''
  In-place update of an intbv with the value of another one.
  '''
  for n in range(len(a)):
    a[n] = b[n]


def int2addr(i):
  return intbv(i, min=0, max=ADDRESS_MAX+1)


def low(i):
  i = ibv(i)
  return i[8:]


def high(i):
  i = ibv(i)
  return i[16:8]


def ibv(i):
  if isinstance(i, (int, long)):
    return intbv(i)
  if not isinstance(i, intbv):
    raise ValueError
  return i


def compute_dw(values):
  accumulator = []
  for value in values:
    accumulator.append(pack('H', value))
  return ''.join(accumulator)


def compute_db(values):
  accumulator = []
  for value in values:
    if isinstance(value, str):
      accumulator.append(value)
    elif isinstance(value, int):
      accumulator.append(pack('B', value))
  data = ''.join(accumulator)
  if len(data) % 2:
    data = data + '\0'
  return data


def instr(method):
  op = method.__name__

  @wraps(method)
  def inner(self, arg0=None, arg1=None):
    addr = self._get_here()

    if arg0 is None:
      assert arg1 is None
      print 'assembling %s instruction at %s' % (op, addr)
      instruction = (op,)
      method(self)

    elif arg1 is not None:
      arg0, arg1 = method(self, arg0, arg1)
      tname, taddress = self._name_or_addr(arg0)
      name, address = self._name_or_addr(arg1)
      print 'assembling %s instruction at %s %s <- %s' % (op, addr, tname, name)
      instruction = (op, taddress, address)

    else:
      arg0 = method(self, arg0)
      name, address = self._name_or_addr(arg0)
      print 'assembling %s instruction at %s to %s' % (op, addr, name)
      instruction = (op, address)

    self.data[addr] = instruction
    self.here += 2

  return inner


def spec(method):
  @wraps(method)
  def inner(self, ptr, register):
    op = method.__name__
    if ptr == 26:
      op = op + '_X'
    elif ptr == 28:
      op = op + '_Y'
    elif ptr == 30:
      op = op + '_Z'
    else:
      raise Exception("Invalid target for %s: %#x" % (op, ptr,))
    self._one(op, register)
  return inner


def spec_reversed(method):
  method = spec(method)
  @wraps(method)
  def inner(self, ptr, register):
    return method(self, register, ptr)
  return inner


def A(func):
  @wraps(func)
  def inner(address):
    return K(func.__doc__, k=address >> 1)
  return inner


def B(func):
  @wraps(func)
  def inner(register, address):
    return K(func.__doc__, d=register, k=address >> 1)
  return inner


def B_reversed(func):
  @wraps(func)
  def inner(address, register):
    return K(func.__doc__, d=register, k=address >> 1)
  return inner


def C(func):
  @wraps(func)
  def inner(io_port, register):
    return K(func.__doc__, a=io_port, r=register)
  return inner


def D(func):
  @wraps(func)
  def inner(Rd, Rr):
    return K(func.__doc__, d=Rd, r=Rr)
  return inner


def E(func):
  @wraps(func)
  def inner(Rr, bit):
    return K(func.__doc__, r=Rr, b=bit)
  return inner


def F(func):
  @wraps(func)
  def inner(Rr):
    return K(func.__doc__, r=Rr)
  return inner


def G(func):
  @wraps(func)
  def inner(Rd):
    return K(func.__doc__, d=Rd)
  return inner


def H(func):
  @wraps(func)
  def inner(register, bit):
    return K(func.__doc__, A=register, b=bit)
  return inner


def K(pattern, **values):
  counts = dict((variable_letter, 0) for variable_letter in values)
  p = ''.join(pattern.lower().split())[::-1]
  n = len(p)
  assert n in (16, 32), repr(pattern)
  accumulator = []
  for i, bit in enumerate(p):
    if bit in '10':
      accumulator.append(bool(int(bit)))
      continue
    assert bit in values, repr((i, bit, values))
    index, value = counts[bit], values[bit]
    counts[bit] += 1
    bit = value[index]
    accumulator.append(bit)
  data = concat(*reversed(accumulator))
  return n, data
