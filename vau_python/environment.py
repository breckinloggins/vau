__author__ = 'bloggins'

from .types import List, Number, Symbol


class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env"""
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def __setitem__(self, key, value):
        # NOTE: not perfect
        if key == '_':
            return

        super(Env, self).__setitem__(key, value)

    def find(self, var):
        """Find the innermost Env where var appears"""
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            return None


def _do_print(x):
    print(x)


def standard_env():
    """An environment with some vau standard procedures"""
    import math
    import operator as op
    env = Env()

    # TODO: Expose host environment and do these within vau
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'append': op.add,
        'begin': lambda *x: x[-1],
        'first': lambda x: x[0],
        'rest': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'list': lambda *x: List(x),
        'list?': lambda x: isinstance(x, List),
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'symbol?': lambda x: isinstance(x, Symbol),
        'print': _do_print,
    })

    return env


global_env = standard_env()
current_env = global_env
