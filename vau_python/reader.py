__author__ = 'bloggins'

from .types import Symbol, List

syntax_forms = []


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

        return read_atom(token)


def read_atom(token):
    """Numbers become Python numbers; every other token is a symbol"""
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
    else:
        return str(exp)


def tokenize(chars):
    """Convert a string of characters into a list of tokens"""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()