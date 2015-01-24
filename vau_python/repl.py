# -*- coding: utf-8 -*-
__author__ = 'bloggins'

from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import CommandLineInterface, AbortAction
from prompt_toolkit import Exit
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.prompt import DefaultPrompt

from .interpreter import vau_builtins, evau
from .lexer import VauLexer
from .reader import parse, vau_str

vau_completer = WordCompleter([k for k in vau_builtins])

VauLexer.keywords = [k for k in vau_builtins]
cli = CommandLineInterface(
    layout=Layout(
        before_input=DefaultPrompt('vau> '),
        menus=[],
        lexer=VauLexer),
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

