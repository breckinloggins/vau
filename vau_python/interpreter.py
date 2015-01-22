__author__ = 'bloggins'

import __builtin__

from .combiners import Syntaxitive, Operative, Applicative
from .types import Symbol, List
from .environment import global_env
from .reader import syntax_forms


def __evau_builtin_platform_object(x, env):
    try:
        (_, name) = x
        val = locals().get(name, None)
        if val is None:
            val = globals().get(name, None)
        if val is not None:
            return val
        else:
            return getattr(__builtin__, name)
    except AttributeError as e:
        raise SyntaxError(e)


def __evau_builtin_defsyntax(x, env):
    # TODO: Break this out into a "syntax lambda" so "def" remains the primitive
    (_, name, parms, body) = x
    form = Syntaxitive(name, parms, body, env, evau)
    syntax_forms.append(form)
    return None


def __evau_builtin_unquote(x, env):
    (_, exp) = x
    return evau(exp, env)


def __evau_builtin_if(x, env):
    (_, test, conseq, alt) = x
    exp = (conseq if evau(test, env) else alt)
    return evau(exp, env)


def __evau_builtin_def(x, env):
    (_, var, exp) = x
    start_sigil = var[0]
    if start_sigil not in ['$', '@', '%']:
        raise SyntaxError("symbol '%s' is invalid; definitions must start with a '$', '@', or '%%'" % var)

    val = evau(exp, env)

    # TODO: Pull this out into its own syntactic meta-feature programmable from vau itself
    if isinstance(val, Applicative):
        if start_sigil != '@':
            raise SyntaxError("symbol '%s' is invalid; symbols that name applicatives must start with '@'" % var)
    elif isinstance(val, Operative):
        if start_sigil != '$':
            raise SyntaxError("symbol '%s' is invalid; symbols that name operatives must start with '$'" % var)
    elif isinstance(val, Syntaxitive):
        if start_sigil != '#':
            raise SyntaxError("symbol '%s' is invalid; symbols that name syntaxitives must start with '#'" % var)
    env[var] = val


def __evau_builtin_set(x, env):
    try:
        (_, var, exp) = x
        env.find(var)[var] = evau(exp, env)
    except AttributeError:
        raise SyntaxError("symbol '%s' is not bound in this environment" % var)


def __evau_builtin_vau(x, env):
    # TODO: This is NOT the correct signature
    (_, parms, body) = x
    return Operative(parms, body, env, evau)


def __evau_builtin_wrap(x, env):
    (_, combiner) = x
    combiner = evau(combiner, env)
    return Applicative(combiner.parms, combiner.body, combiner.env, combiner.evau)


def __evau_builtin_fn(x, env):
    (_, parms, body) = x
    return Applicative(parms, body, env, evau)


vau_builtins = {
    '$platform-object': __evau_builtin_platform_object,
    '$defsyntax!': __evau_builtin_defsyntax,
    '$unquote': __evau_builtin_unquote,
    '$if': __evau_builtin_if,
    '$def!': __evau_builtin_def,
    '$set!': __evau_builtin_set,
    '$vau': __evau_builtin_vau,
    '$fn': __evau_builtin_fn,
    '@wrap': __evau_builtin_wrap,
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
    elif isinstance(x[0], Symbol) and x[0] in vau_builtins:
        try:
            return vau_builtins[x[0]](x, env)
        except ValueError:
            raise SyntaxError("incorrect number of arguments to '%s'" % x[0])
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
