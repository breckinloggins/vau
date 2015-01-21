# Initial lisp interpreter based heavily on http://norvig.com/lispy.html
__author__ = 'bloggins'


import sys

Symbol = str
List = list
Number = (int, float)


class Combiner(object):
    """A user-defined vau combination"""
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return evau(self.body, Env(self.parms, args, self.env))


class Operative(Combiner):
    pass


class Applicative(Combiner):
    pass


class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env"""
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """Find the innermost Env where var appears"""
        return self if (var in self) else self.outer.find(var)


def do_evau(x, env):
    evau(x, env)


def do_print(x):
    print x


def standard_env():
    """An environment with some vau standard procedures"""
    import math, operator as op
    env = Env()

    # TODO: Expose host environment and do these within vau
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': apply,
        'begin': lambda *x: x[-1],
        'first': lambda x: x[0],
        'rest': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: List(x),
        'list?': lambda x: isinstance(x, List),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
        'print': do_print,
        '#quit': lambda: sys.exit(1),

        # How meta
        'evau': do_evau,
    })

    return env


global_env = standard_env()


def repl(prompt='vau> '):
    """The vau read-evau-print loop"""
    from pygments.lexers.lisp import SchemeLexer

    from prompt_toolkit import CommandLineInterface, AbortAction
    from prompt_toolkit import Exit
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.prompt import DefaultPrompt

    cli = CommandLineInterface(layout=Layout(
        before_input=DefaultPrompt(prompt),
        lexer=SchemeLexer
    ))

    try:
        while True:
            code_obj = cli.read_input(on_exit=AbortAction.RAISE_EXCEPTION)
            try:
                val = evau(parse(code_obj.text))
                print(vaustr(val))
            except SyntaxError as e:
                print "error: %s" % e
    except Exit:
        return


def evau(x, env=global_env):
    """Evaluate an expression in an environment"""
    if isinstance(x, Symbol):
        try:
            return env.find(x)[x]
        except (KeyError, AttributeError):
            raise SyntaxError("symbol '%s' is not bound in this environment" % x)
    elif not isinstance(x, List):
        return x
    elif len(x) == 0:
        return x
    elif x[0] == 'quote':
        try:
            (_, exp) = x
            return exp
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'quote'")
    elif x[0] == 'unquote':
        try:
            (_, exp) = x
            return evau(exp, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'unquote'")
    elif x[0] == 'if':
        try:
            (_, test, conseq, alt) = x
            exp = (conseq if evau(test, env) else alt)
            return evau(exp, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'if'")
    elif x[0] == 'def':
        try:
            (_, var, exp) = x
            env[var] = evau(exp, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'def'")
    elif x[0] == 'set!':
        try:
            (_, var, exp) = x
            env.find(var)[var] = evau(exp, env)
        except AttributeError:
            raise SyntaxError("symbol '%s' is not bound in this environment" % var)
    elif x[0] == 'vau':
        try:
            (_, parms, body) = x
            return Operative(parms, body, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'vau'")
    elif x[0] == 'fn':
        try:
            (_, parms, body) = x
            return Applicative(parms, body, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'fn'")
    else:
        try:
            proc = evau(x[0], env)
            if not callable(proc):
                raise SyntaxError("'%s' is not callable" % proc)
            if isinstance(proc, Operative):
                args = [arg for arg in x[1:]]
            else:
                args = [evau(arg, env) for arg in x[1:]]

            return proc(*args)
        except Exception as e:
            raise SyntaxError(e)
        return x


def parse(program):
    """Read a vau representation from a string"""
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):
    """Read an expression from a sequence of tokens"""
    if len(tokens) == 0:
        raise SyntaxError("unexpected end of input while reading")

    token = tokens.pop(0)
    if '(' == token:
        read_list = []
        while len(tokens) != 0 and tokens[0] != ')':
            read_list.append(read_from_tokens(tokens))

        try:
            tokens.pop(0)   # pops off the last ')' we read
        except IndexError:
            raise SyntaxError("expected ')' while reading")

        return read_list
    elif ')' == token:
        raise SyntaxError("unexpected ')' while reading")
    else:
        return atom(token)


def tokenize(chars):
    """Convert a string of characters into a list of tokens"""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def atom(token):
    """Numbers become Python numbers; every other token is a symbol"""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def vaustr(exp):
    """Convert Python object back into a vau-readable string"""
    if isinstance(exp, List):
        return '(' + ' '.join(map(vaustr, exp)) + ')'
    else:
        return str(exp)


def main():
    print "vau: a lisp. (type #quit to quit)"
    repl()

if __name__ == "__main__":
    main()
