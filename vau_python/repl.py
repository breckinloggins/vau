# -*- coding: utf-8 -*-
from prompt_toolkit.layout.utils import TokenList

__author__ = 'bloggins'

from pygments.token import Token, Generic

from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import CommandLineInterface, AbortAction
from prompt_toolkit import Exit
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.prompt import DefaultPrompt

from .interpreter import vau_builtins, evau
from .lexer import VauLexer, VauStyle
from .reader import parse, vau_str

vau_completer = WordCompleter([k for k in vau_builtins])
VauLexer.keywords = [k for k in vau_builtins]


class BracketsMismatchProcessor(object):
    """
    Processor that replaces the token type of bracket mismatches by an Error.
    """
    error_token = Generic.Inserted

    def process_tokens(self, tokens):
        tokens = list(TokenList(tokens))

        stack = []  # Pointers to the result array

        for index, (token, text) in enumerate(tokens):
            top = tokens[stack[-1]][1] if stack else ''

            if text in '({[]})':
                if text in '({[':
                    # Put open bracket on the stack
                    stack.append(index)

                elif (text == ')' and top == '(' or
                      text == '}' and top == '{' or
                      text == ']' and top == '['):
                    # Match found
                    stack.pop()
                else:
                    # No match for closing bracket.
                    tokens[index] = (self.error_token, text)

        # Highlight unclosed tags that are still on the stack.
        for index in stack:
            tokens[index] = (self.error_token, tokens[index][1])

        return tokens



cli = CommandLineInterface(
    layout=Layout(
        input_processors=[BracketsMismatchProcessor()],
        before_input=DefaultPrompt(u'ϛ '),
        menus=[],
        lexer=VauLexer),
    style=VauStyle,
    buffer=Buffer(completer=vau_completer),
    create_async_autocompleters=True,
)


def start_repl():
    """The vau read-evau-print loop"""
    try:
        while True:
            code_obj = cli.read_input(on_exit=AbortAction.RAISE_EXCEPTION)
            try:
                val = evau(parse(code_obj.text, evau))
                print(vau_str(val))
            except SyntaxError as e:
                print "error: %s" % e
    except Exit:
        return

