# Initial lisp interpreter based heavily on http://norvig.com/lispy.html

__author__ = 'bloggins'


import sys

Symbol = str
List = list
Number = (int, float)
Env = dict


def standard_env():
    """An environment with some vau standard procedures"""
    import math, operator as op
    env = Env()
    env.update(vars(math))

    return env


global_env = standard_env()


def eval(x, env=global_env):
    """Evaluate an expression in an environment"""
    if isinstance(x, Symbol):
        try:
            return env[x]
        except KeyError:
            raise SyntaxError("symbol '%s' is not bound in this environment" % x)
    else:
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


def main():

    print "vau: a lisp. (type #quit to quit)"
    while 1:
        print "vau> ",
        input_line = sys.stdin.readline().rstrip('\n')
        if input_line == "#quit":
            break

        try:
            vau_program = eval(parse(input_line))
            print "%s" % vau_program
        except SyntaxError as e:
            print "error: %s" % e

if __name__ == "__main__":
    main()
