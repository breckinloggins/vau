from pygments.token import Text

__author__ = 'bloggins'

import os

from .types import Symbol, List, String, symbol_prefixes
from .environment import syntax_forms, global_env, Env
from .lexer import VauLexer

current_lexer = None


def set_current_lexer(lexer):
    global current_lexer
    current_lexer = lexer


def load_file(filename, evau_fn=None, static_env=global_env):
    with open(os.path.realpath(filename)) as vau_file:
        contents = vau_file.read().replace('\n', ' ')
        tokens = tokenize(contents)
        while len(tokens) > 0:
            evau_fn(read_from_tokens(tokens, evau_fn, static_env))


def parse(program, evau_fn=None, static_env=global_env):
    """Read a vau representation from a string"""
    return read_from_tokens(tokenize(program), evau_fn, static_env)


def read_from_tokens(tokens, evau_fn=None, static_env=global_env):
    """Read an expression from a sequence of tokens"""
    if len(tokens) == 0:
        raise SyntaxError("unexpected end of input while reading")

    while True:
        token = tokens.pop(0)
        if not token.isspace():
            break

    if '(' == token:
        read_list = []
        while len(tokens) != 0 and tokens[0] != ')':
            read_list.append(read_from_tokens(tokens, evau_fn, static_env))

        try:
            tokens.pop(0)   # pops off the last ')' we read
        except IndexError:
            raise SyntaxError("expected ')' while reading")

        # Lexical macro expansion happens here
        if len(read_list) > 0 and isinstance(read_list[0], Symbol) and read_list[0][0] not in symbol_prefixes:
            sym = read_list[0]
            sym = Symbol("^%s" % sym)
            sym_env = static_env.find(sym)
            if sym_env is not None:
                if evau_fn is None:
                    raise SyntaxError("cannot evaluate macro expression '%s' in this context because the reader does not have an evaluator" % sym_env)
                macro = sym_env[sym]
                read_list[0] = macro
                return evau_fn(read_list, Env(outer=static_env))

        return read_list
    elif ')' == token:
        raise SyntaxError("unexpected ')' while reading")
    else:
        for form in syntax_forms:
            val = form.maybe_read(token, tokens)
            if val is not None:
                return val

        atom = read_atom(token)

        # TODO: Do this in vau when we have greater reader extensibility
        # if isinstance(atom, Symbol):
        #     if '/' in atom:
        #         parts = atom.split('/')
        #         if len(parts) != 2:
        #             raise SyntaxError("symbol ('%s') has too many '/' characters. Only 0 or 1 supported." % atom)
        #         env_part = parse(parts[0], evau_fn, static_env)
        #         exp_part = parse(parts[1], evau_fn, static_env)
        #         return [Symbol("@evau"), exp_part, env_part]

        return atom

def read_atom(token):
    """Numbers become Python numbers; every other token is a symbol or a string"""
    if len(token) >= 2 and token[0] == '"' and token[-1] == '"':
        return String(token.strip('"'))

    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def vau_str(exp):
    """Convert Python object back into a vau-readable string"""
    if isinstance(exp, List):
        return '(' + ' '.join(map(vau_str, exp)) + ')'
    elif isinstance(exp, String):
        return '"' + exp + '"'
    else:
        return str(exp)


def tokenize(chars):
    """Convert a string of characters into a list of tokens"""
    token_iterator = current_lexer.get_tokens(chars)
    tokens = [value for (token, value) in token_iterator if token != Text.Whitespace]
    return tokens
