#!/usr/bin/env python
'''
Playing with integrating la.py and co.py

So this is basically an attempt to understand:

"Accessible Language-Based Environments of Recursive Theories", Ian
Piumarta - http://www.vpri.org/pdf/rn2006001a_colaswp.pdf

by implementing [part of] it in python. The co module implements the
object model as simply and directly as I could, and the la module tries
to implement the transformation engine using that object module.

I'm not quite getting it.  This works, but I think there's a much more
elegant system just out of sight and the secret's in the way you dispatch
the transform method to objects vs symbols. I'm not sure though.

This is a somewhat more elegant take on rootbeer.py, I'm still not quite
getting it though.

The following classes/methods are constructed.

    Object.eval
    Object.transform
    Object.typeOf

    Symbol.transform
    Symbol.setName / Symbol.getName
    Symbol.setSymbol

    AST.init

'''
from co import send


def Eval(tree, context):
    symbol = send(tree, 'typeOf')
    closure = send(symbol, 'transform', context)
    new_tree = closure(tree, context)
    if new_tree is not None:
        return send(new_tree, 'eval', context)


def setName(symbol, name):
    symbol.name = name
    return symbol
def getName(symbol): return symbol.name


def setSymbol(symbol, thing):
    thing.symbol = symbol
    return symbol
def getSymbol(obj): return obj.symbol # aka typeOf


def transform(symbol, context):
    return send(context, 'lookup', send(symbol, 'getName'))


def init_ast(ast, symbol, value):
    ast.data = value
    send(symbol, 'setSymbol', ast)
    return ast


# At this point the basic eval/transform widgetry is done. It still needs
# some cruft to work though: ASTs and symbols to attach to the ASTs.

def setUpTransformEngine(object_vt, vtvt):

    # Create a Symbol object type.
    symbol_vt = send(vtvt, 'delegated')

    # Create ast object type.
    ast_vt = send(object_vt, 'delegated')

    send(object_vt, 'addMethod', 'eval', Eval)
    send(object_vt, 'addMethod', 'transform', Eval)
    send(object_vt, 'addMethod', 'typeOf', getSymbol)

    send(symbol_vt, 'addMethod', 'setName', setName)
    send(symbol_vt, 'addMethod', 'getName', getName)
    send(symbol_vt, 'addMethod', 'setSymbol', setSymbol)
    send(symbol_vt, 'addMethod', 'transform', transform)

    send(ast_vt, 'addMethod', 'init', init_ast)

    return symbol_vt, ast_vt
