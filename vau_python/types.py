__author__ = 'bloggins'


class Symbol(unicode):
    pass


class String(unicode):
    pass


List = list

# TODO: Numbers and strings should NOT be primitive. They should be exposed and encapsulated from the platform
Number = (int, float)

symbol_prefixes = ['#', '^']
