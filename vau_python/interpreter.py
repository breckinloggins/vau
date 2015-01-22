__author__ = 'bloggins'

import __builtin__

from .combiners import Syntaxitive, Operative, Applicative
from .types import Symbol, List
from .environment import global_env
from .reader import syntax_forms


vau_builtins = {
    '$platform-object',
    '$defsyntax!',
    '$unquote',
    '$if',
    '$def!',
    '$set!',
    '$vau',
    '$fn',
    'wrap',
}


def evau(x, env=global_env):
    """Evaluate an expression in an environment"""
    if isinstance(x, Symbol):
        try:
            return env.find(x)[x]
        except (KeyError, TypeError, AttributeError):
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
            form = Syntaxitive(name, parms, body, env, evau)
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
            return Operative(parms, body, env, evau)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '$vau'")
    elif x[0] == 'wrap':
        try:
            (_, combiner) = x
            combiner = evau(combiner, env)
            return Applicative(combiner.parms, combiner.body, combiner.env, combiner.evau)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to 'wrap'")
    elif x[0] == '$fn':
        try:
            (_, parms, body) = x
            return Applicative(parms, body, env, evau)
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
