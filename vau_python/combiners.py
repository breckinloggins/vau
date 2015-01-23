__author__ = 'bloggins'

from .environment import Env
from .types import Symbol, List
from .reader import read_from_tokens


def subst(x, name, replacement):
    if isinstance(x, Symbol) and x == name:
        return replacement
    elif isinstance(x, List):
        return [subst(el, name, replacement) for el in x]
    else:
        return x


class Combiner(object):
    """A user-defined vau combination"""
    def __init__(self, parms, body, env, evau):
        self.parms, self.body, self.env, self.evau = parms, body, env, evau

    def __call__(self, *args):
        return self.evau(self.body, Env(self.parms, args, self.env))


class Operative(Combiner):
    """A combiner that does not evaluate its arguments"""
    def __init__(self, parms, eparm, body, env, evau):
        if eparm in parms and eparm != '_':
            raise SyntaxError("parameter name '%s' cannot be both a formal parameter and an environment parameter")

        self.parms, self.eparm, self.body, self.env, self.evau = parms, eparm, body, env, evau

    def __call__(self, dyn_env, *args):
        if not isinstance(dyn_env, Env):
            raise SyntaxError('first parameter given to operative call must be an environment')
        local_env = Env(self.parms, args, self.env)
        local_env[self.eparm] = dyn_env
        return self.evau(self.body, local_env)


class Applicative(Combiner):
    """A combiner that does evaluate its arguments"""
    pass


class Syntaxitive(Combiner):
    """A combiner that influences the reader"""
    def __init__(self, name, parms, body, env, evau):
        if not name.startswith('#'):
            raise SyntaxError("symbol '%s' is invalid; syntaxitives must start with a '#'" % name)

        self.name, self.parms, self.body, self.env, self.evau = name[1:], parms, body, env, evau
        self.parts = self.name.split('`')

        if len(self.parms) != 1:
            raise SyntaxError("syntax forms with 0 or more than one argument are not yet supported")
        if len(self.parts) != 2 or self.parts[1] != '':
            raise SyntaxError("syntax forms must begin with a symbol and end with a '`'")
        if self.parts[0] == '':
            raise SyntaxError("syntax forms beginning with '`' are not yet supported")

    def maybe_read(self, next_token, tokens):
        if len(next_token) == 0:
            return None

        if not next_token.startswith(self.parts[0]):
            return None

        new_token = next_token[len(self.parts[0]):]
        if new_token != '':
            tokens.insert(0, new_token)
        expr = read_from_tokens(tokens, self.evau)
        if expr is None:
            raise SyntaxError("expected expression after '%s'" % self.parts[0])

        val = subst(self.body, self.parms[0], expr)
        #val = self(expr)
        return val
