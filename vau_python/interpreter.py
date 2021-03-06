__author__ = 'bloggins'

import __builtin__

from .combiners import Syntaxitive, Operative
from .types import Symbol, List, symbol_prefixes
from .environment import global_env, syntax_forms, Env


def __evau_builtin_python_object(env, name):
    try:
        val = locals().get(name, None)
        if val is None:
            val = globals().get(name, None)
        if val is None:
            val = getattr(__builtin__, name)

        # if val is not None and hasattr(val, '__call__'):
        #     # Need to wrap this call because it won't be expecting
        #     # to take an environment or unevaluated operands
        #     val = __evau_builtin_raw_wrap(env, val)

        return val

    except AttributeError as e:
        raise SyntaxError(e)


def __evau_builtin_syntax_as(env, name, parms_or_exp, body=None):
    # TODO: Break this out into a "syntax lambda" so "::" remains the primitive
    start_sigil = name[0]
    if start_sigil not in symbol_prefixes:
        raise SyntaxError("symbol '%s' is invalid; syntaxitives must begin with %s" % (name, symbol_prefixes))

    if start_sigil == '^':
        if body is not None:
            raise SyntaxError("syntaxitive '%s' cannot take additional parameters" % name)
        val = evau(parms_or_exp, env)
        env[name] = val
    else:
        if body is None:
            raise SyntaxError("syntaxitive '%s' needs a body" % name)
        val = Syntaxitive(name, parms_or_exp, body, env, evau)
        syntax_forms.append(val)

    return val


def __evau_builtin_cond(env, *x):
    args = list(x)
    args.append(None)
    for test, exp in zip(args[::2], args[1::2]):
        test_val = evau(test, env)
        if test_val:
            if exp is None:
                return test_val
            else:
                return evau(exp, env)

    raise SyntaxError("improper arguments to cond")


def __evau_builtin_as(env, var, exp):
    start_sigil = var[0]
    if start_sigil in symbol_prefixes:
        raise SyntaxError("symbol '%s' is invalid; definitions must not begin with %s" % (var, symbol_prefixes))

    val = evau(exp, env)
    env[var] = val


def __evau_builtin_let_as(env, var, exp):
    try:
        env.find(var)[var] = evau(exp, env)
    except AttributeError:
        raise SyntaxError("symbol '%s' is not bound in this environment" % var)


def __evau_builtin_vau(env, parms, eparm, body):
    return Operative(parms, eparm, body, env, evau)


def __evau_builtin_wrap(env, exp):
    exp = evau(exp, env)
    return lambda v, *x: exp(v, *[evau(expr, v) for expr in x])


def __evau_builtin_raw_wrap(env, exp):
    # Like wrap but does not call with the environment. Useful for calls into
    # the platform layer and other such low-level work
    exp = evau(exp, env)
    return lambda v, *x: exp(*[evau(expr, v) for expr in x])


def __evau_builtin_evau(env, exp, new_env):
    exp = evau(exp, env)
    new_env = evau(new_env, env)
    if not isinstance(new_env, Env):
        raise SyntaxError("second argument to evau must evaluate to an environment")
    return evau(exp, new_env)


def __evau_builtin_present(env, x):
    print(evau(x, env))


vau_builtins = {
    'python-object': __evau_builtin_python_object,
    'syntax::': __evau_builtin_syntax_as,
    'cond': __evau_builtin_cond,
    '::': __evau_builtin_as,
    'let::': __evau_builtin_let_as,
    'vau': __evau_builtin_vau,
    'wrap': __evau_builtin_wrap,
    'raw-wrap': __evau_builtin_raw_wrap,
    'evau': __evau_builtin_evau,

    'present': __evau_builtin_present,

    'op-add': lambda v, x, y: evau(x, v) + evau(y, v),
    'True': True,
    'False': False,
    # 'begin': lambda *x: x[-1],
    # 'car': lambda x: x[0],
    # 'cdr': lambda x: x[1:],
    # 'cons': lambda x, y: [x] + y,
    # 'eq?': op.is_,
    # 'equal?': op.eq,
    'list': lambda v, *x: List([evau(expr, v) for expr in x]),
    # 'list?': lambda x: isinstance(x, List),
    # 'not': op.not_,
    # 'null?': lambda x: x == [],
    # 'number?': lambda x: isinstance(x, Number),
    # 'symbol?': lambda x: isinstance(x, Symbol),

}

global_env.update(vau_builtins)


def evau(x, env=global_env):
    """Evaluate an expression in an environment"""
    if isinstance(x, Symbol):
        try:
            return env.find(x)[x]
        except (KeyError, TypeError, AttributeError):
            raise SyntaxError("symbol '%s' is not bound in this environment" % x)
    elif isinstance(x, List):
        if len(x) == 0:
            return x

        proc = evau(x[0], env)
        if hasattr(proc, '__call__'):
            try:
                return proc(env, *x[1:])
            except Exception as e:
                raise SyntaxError(e)

        raise SyntaxError("%s is not callable" % str(proc))
    else:
        return x
