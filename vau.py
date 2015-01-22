from __future__ import unicode_literals

# Initial lisp interpreter based heavily on http://norvig.com/lispy.html
__author__ = 'bloggins'

import sys
import __builtin__
from prompt_toolkit.contrib.completers import WordCompleter

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
    """A combiner that does not evaluate its arguments"""
    pass


class Applicative(Combiner):
    """A combiner that does evanulate its arguments"""
    pass


class Syntaxitive(Combiner):
    """A combiner that influences the reader"""
    def __init__(self, name, parms, body, env):
        self.name, self.parms, self.body, self.env = name, parms, body, env
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
        expr = read_from_tokens(tokens)
        if expr is None:
            raise SyntaxError("expected expression after '%s'" % self.parts[0])

        return subst(self.body, self.parms[0], expr)


class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env"""
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """Find the innermost Env where var appears"""
        return self if (var in self) else self.outer.find(var)


def subst(x, name, replacement):
    if isinstance(x, Symbol) and x == name:
        return replacement
    elif isinstance(x, List):
        return [subst(el, name, replacement) for el in x]
    else:
        return x

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
        'print': do_print,

        # How meta
        'evau': do_evau,
    })

    return env


global_env = standard_env()
syntax_forms = []


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
    elif x[0] == '$platform-object':
        try:
            (_, name) = x
            val = locals().get(name, None)
            if val is None:
                val = globals().get(name, None)
            if val is not None:
                return val
            else:
                return getattr(__builtin__, name)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$platform-object'")
        except AttributeError as e:
            raise SyntaxError(e)
    elif x[0] == '$defsyntax!':
        # TODO: Break this out into a "syntax lambda" so "def" remains the primitive
        try:
            (_, name, parms, body) = x
            form = Syntaxitive(name, parms, body, env)
            syntax_forms.append(form)
            return None
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$defsyntax!'")
    elif x[0] == '$unquote':
        try:
            (_, exp) = x
            return evau(exp, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$unquote'")
    elif x[0] == '$if':
        try:
            (_, test, conseq, alt) = x
            exp = (conseq if evau(test, env) else alt)
            return evau(exp, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$if'")
    elif x[0] == '$def!':
        try:
            (_, var, exp) = x
            env[var] = evau(exp, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$def!'")
    elif x[0] == '$set!':
        try:
            (_, var, exp) = x
            env.find(var)[var] = evau(exp, env)
        except AttributeError:
            raise SyntaxError("symbol '%s' is not bound in this environment" % var)
    elif x[0] == '$vau':
        # TODO: This is NOT the correct signature
        try:
            (_, parms, body) = x
            return Operative(parms, body, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$vau'")
    elif x[0] == 'wrap':
        try:
            (_, combiner) = x
            combiner = evau(combiner, env)
            return Applicative(combiner.parms, combiner.body, combiner.env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'wrap'")
    elif x[0] == '$fn':
        try:
            (_, parms, body) = x
            return Applicative(parms, body, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$fn'")
    else:
        try:
            proc = evau(x[0], env)
            if isinstance(proc, dict) and not callable(proc):
                # Dicts are functions of their keys
                args = [evau(arg, env) for arg in x[1:]]
                if len(args) == 1:
                    return proc.get(args[0])
                else:
                    return [proc.get(arg) for arg in args]
            elif not callable(proc):
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
        for form in syntax_forms:
            val = form.maybe_read(token, tokens)
            if val is not None:
                return val

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


prologue = """
($def! $quote ($vau (x) x))
($defsyntax! '` (x) ($quote x))
($defsyntax! .` (x) ($platform-object x))
"""


def main():
    print "vau: a lisp. (type (.exit) to quit)"
    for line in prologue.splitlines():
        if len(line) == 0:
            continue
        evau(parse(line))
    repl()

if __name__ == "__main__":
    main()
