'''

A simple model of an Object Model as per:

"Open Reusable Object Models", Ian Piumarta, Alessandro Warth
http://www.vpri.org/pdf/tr2006003a_objmod.pdf

This departs in several ways from the OM described in that paper. It's
meant mainly as a rough sketch done to better understand the ideas.

There is no specific symbol type, we just use strings. The vtable also
has no specific type, it's just an Object.  Last, I lean on the python
dict type to act as the vtable's storage.
'''

class Object:
    '''
    Root of the whole system, has a vtable and some data.
    '''
    def __init__(self, vtable):
        self.vtable = vtable
        self.data = None
    def __repr__(self):
##        return '<co.Object(%r) of type %r>' % (self.data,
##                                               'O' if self.vtable is self else self.vtable.data.keys() )
        return '<co.Object(%r)>' % (self.data,)

def send(obj, name, *args, **keyword_args):
    method = bind(obj, name)
    return method(obj, *args, **keyword_args)

def bind(obj, name):
    if obj.vtable is obj and name == 'lookup':
        return lookup(obj, name)
    return send(obj.vtable, 'lookup', name)

def addMethod(vtable, name, implementation):
    vtable.data[name] = implementation

def lookup(vtable, name):
    try:
        return vtable.data[name]
    except KeyError:
        if vtable.parent is not None:
            return send(vtable.parent, 'lookup', name)
        raise Exception("lookup failed for %r" % name)

def delegated(vtable):
    vt = None if vtable is None else vtable.vtable
    child = Object(vt) # allocate() from the paper.
    child.parent = vtable
    child.data = {} # Map names to methods.
    return child


def bootstrap():

    # Create the VTable's VTable.
    vtvt = delegated(None)

    # VTable is its own VTable.
    vtvt.vtable = vtvt

    # Create a VTable for Objects. (Use delegated(None) so it has no
    # parent.  In other words Object, not VTable, is the root of the
    # system.)
    object_vt = delegated(None)

    # Manually tell it it's a VTable.
    object_vt.vtable = vtvt

    # VTable is a kind of Object. Thus its VTable's parent is Object's
    # VTable and since it's its own VTable we just set its parent here.
    vtvt.parent = object_vt

    # Give VTable a lookup method by directly calling addMethod().
    addMethod(vtvt, 'lookup', lookup)

    # Now the send() and bind() machinery will work.
    assert lookup is send(vtvt, 'lookup', 'lookup')

    # Add addMethod() to the VTable.
    addMethod(vtvt, 'addMethod', addMethod)

    # We can add the rest using send().
    send(vtvt, 'addMethod', 'allocate', Object) # Use class as allocate().
    send(vtvt, 'addMethod', 'delegated', delegated)

    # We're done.
    return object_vt, vtvt

