'''
Stack
=================================

Tuple-based persistent stack.

This is too simple to document.  It's almost too simple to implement.
'''


def push(stack, *items):
    '''Push arguments onto a stack.'''
    for item in items:
        stack = item, stack # push
    return stack


def pop(stack, number):
    '''Pop number arguments from stack.'''
    for _ in range(number):
        item, stack = stack # pop
        yield item
    yield stack


def iterStack(stack):
    '''Iterate through the items on the stack.'''
    while stack:
        item, stack = stack
        yield item


def lenStack(stack):
    '''Return the number of items on the stack.'''
    return sum(1 for _ in iterStack(stack))


def pick_(stack, n):
    '''
    Find the nth item on the stack and duplicate it to TOS. (Pick with
    zero is the same as "dup".)
    '''
    if n < 0:
        raise ValueError
    s = stack
    while True:
        try:
            item, s = s
        except ValueError:
            raise IndexError
        n -= 1
        if n < 0:
            break
    return item, stack

