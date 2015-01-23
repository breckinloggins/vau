__author__ = 'bloggins'

import __builtin__

from .combiners import Syntaxitive, Operative, Applicative
from .types import Symbol, List, symbol_prefixes
from .environment import global_env, syntax_forms, Env


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


def __evau_builtin_if(x, env):
    (_, test, conseq, alt) = x
    exp = (conseq if evau(test, env) else alt)
    return evau(exp, env)


def __evau_builtin_define(x, env):
    (_, var, exp) = x
    start_sigil = var[0]
    if start_sigil not in symbol_prefixes:
        raise SyntaxError("symbol '%s' is invalid; definitions must start with one of %s" % (var, symbol_prefixes))

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
    elif start_sigil != '%' and start_sigil != '^':
        raise SyntaxError("symbol '%s' is invalid for the type of object (%s) being defined" % (val, type(val)))
    env[var] = val


def __evau_builtin_set(x, env):
    try:
        (_, var, exp) = x
        env.find(var)[var] = evau(exp, env)
    except AttributeError:
        raise SyntaxError("symbol '%s' is not bound in this environment" % var)


def __evau_builtin_vau(x, env):
    (_, parms, eparm, body) = x
    return Operative(parms, eparm, body, env, evau)


def __evau_builtin_wrap(x, env):
    (_, combiner) = x
    combiner = evau(combiner, env)
    return Applicative(combiner.parms, combiner.body, combiner.env, combiner.evau)


def __evau_builtin_fn(x, env):
    (_, parms, body) = x
    return Applicative(parms, body, env, evau)


def __evau_builtin_evau(x, env):
    (_, exp, new_env) = x
    exp = evau(exp, env)
    new_env = evau(new_env, env)
    if not isinstance(new_env, Env):
        raise SyntaxError("second argument to @evau must evaluate to an environment")
    return evau(exp, new_env)


vau_builtins = {
    '$platform-object': __evau_builtin_platform_object,
    '$defsyntax!': __evau_builtin_defsyntax,
    '$if': __evau_builtin_if,
    '$define!': __evau_builtin_define,
    '$set!': __evau_builtin_set,
    '$vau': __evau_builtin_vau,
    '$fn': __evau_builtin_fn,
    '@wrap': __evau_builtin_wrap,
    '@evau': __evau_builtin_evau,
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
                return proc(env, *args)
            else:
                args = [evau(arg, env) for arg in x[1:]]
                return proc(*args)

        except Exception as e:
            raise SyntaxError(e)
        return x
