# -*- coding: utf-8 -*-
__author__ = 'bloggins'

from pygments.lexer import RegexLexer
from pygments.token import Text, Name, Number, Keyword, String, Punctuation, Operator


class VauLexer(RegexLexer):
    """
    A vau lexer, parsing a stream and outputting the tokens
    needed to highlight vau code.
    """

    name = 'vau'
    aliases = ['Vau', 'vau-lang']
    filenames = ['*.vau']
    mimetypes = ['text/x-vau', 'application/x-vau']

    keywords = (

    )

    builtins = (
    )

    # valid names for identifiers
    # well, names can only not consist fully of numbers
    # but this should be good enough for now
    valid_name = r'[\w!$%&*+,/:<=>?@^~|-]+'

    tokens = {
        'root': [
            # the comments
            # and going to the end of the line
            # (r';.*$', Comment.Single),
            # multi-line comment
            # (r'#\|', Comment.Multiline, 'multiline-comment'),
            # commented form (entire sexpr folliwng)
            # (r'#;\s*\(', Comment, 'commented-form'),
            # signifies that the program text that follows is written with the
            # lexical and datum syntax described in r6rs
            # (r'#!r6rs', Comment),

            # whitespaces - usually not relevant
            (r'\n', Text),
            (r'\s+', Text.Whitespace),

            # numbers
            (r'-?\d+\.\d+', Number.Float),
            (r'-?\d+', Number.Integer),
            # support for uncommon kinds of numbers -
            # have to figure out what the characters mean
            # (r'(#e|#i|#b|#o|#d|#x)[\d.]+', Number),

            # strings, symbols and characters
            (r'"(\\\\|\\"|[^"])*"', String),
            # (r"'" + valid_name, String.Symbol),
            # (r"#\\([()/'\"._!§$%& ?=+-]|[a-zA-Z0-9]+)", String.Char),

            # constants
            # (r'(#t|#f)', Name.Constant),

            # special operators
            # (r"('|#|`|,@|,|\.)", Operator),

            # highlight the keywords
            #('(%s)' % '|'.join(re.escape(entry) + ' ' for entry in keywords), Keyword),

            # HACK: This should be handled by some metadata on defsyntax
            (r"\." + valid_name, Name.Constant),
            # (r"@" + valid_name, Name.Function),
            # (r"\$" + valid_name, Keyword),
            (r"#\S+", Operator),
            # (r"%" + valid_name, Name.Entity),
            (r"\^" + valid_name, Name.Exception),

            # first variable in a quoted string like
            # '(this is syntactic sugar)
            # (r"(?<='\()" + valid_name, Name.Variable),
            # (r"(?<=#\()" + valid_name, Name.Variable),

            # highlight the builtins
            # ("(?<=\()(%s)" % '|'.join(re.escape(entry) + ' ' for entry in builtins),
            # Name.Builtin),

            # the remaining functions
            # (r'(?<=\()' + valid_name, Name.Function),
            # find the remaining variables
            (valid_name, Name.Other),

            # the famous parentheses!
            (r'(\(|\))', Punctuation),
            (r'(\[|\])', Punctuation),
        ],
        # 'multiline-comment': [
        #     (r'#\|', Comment.Multiline, '#push'),
        #     (r'\|#', Comment.Multiline, '#pop'),
        #     (r'[^|#]+', Comment.Multiline),
        #     (r'[|#]', Comment.Multiline),
        # ],
        # 'commented-form': [
        #     (r'\(', Comment, '#push'),
        #     (r'\)', Comment, '#pop'),
        #     (r'[^()]+', Comment),
        # ],
    }

    # def get_tokens_unprocessed(self, text):
    #     for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
    #         if token is Name.Other and current_env is not None and current_env.find(value) is not None:
    #             yield index, Keyword.Pseudo, value
    #         else:
    #             yield index, token, value

