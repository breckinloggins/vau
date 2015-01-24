# -*- coding: utf-8 -*-
__author__ = 'bloggins'

from pygments.lexer import RegexLexer
from pygments.style import Style
from pygments.token import Text, Name, Number, Keyword, String, Punctuation, Operator, Comment, Error, Token, Generic


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


class VauStyle(Style):
    background_color = None
    styles = {
        # http://paletton.com/ for a color palette

        # Build-ins from the Pygments lexer.
        Comment:                                      '#0000dd',
        Error:                                        '#000000 bg:#ff8888',
        Keyword:                                      '#ee00ee',
        Name.Decorator:                               '#aa22ff',
        Name.Namespace:                               '#008800 underline',
        Name:                                         '#008800',
        Number:                                       '#ff0000',
        Operator:                                     '#ff6666 bold',
        String:                                       '#ba4444 bold',
        Generic.Inserted:                             'underline',

        # Highlighting of search matches in document.
        Token.SearchMatch:                            '#ffffff bg:#4444aa',
        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',

        # Highlighting of select text in document.
        Token.SelectedText:                           '#ffffff bg:#6666aa',

        # (Vau) Prompt: "vau [1]>"
        Token.Prompt:                                 'bold #008800',

        # Line numbers.
        Token.Layout.LeftMargin:                      '#aa6666',

        # Search toolbar.
        Token.Toolbar.Search:                         '#22aaaa noinherit',
        Token.Toolbar.Search.Text:                    'noinherit',
        Token.Toolbar.Search.Text.NoMatch:            'bg:#aa4444 #ffffff',

        # System toolbar
        Token.Toolbar.System.Prefix:                  '#22aaaa noinherit',

        # "arg" toolbar.
        Token.Toolbar.Arg:                            '#22aaaa noinherit',
        Token.Toolbar.Arg.Text:                       'noinherit',

        # Signature toolbar.
        Token.Toolbar.Signature:                      '#888888',
        Token.Toolbar.Signature.CurrentName:          'bold underline #888888',
        Token.Toolbar.Signature.Operator:             'bold #888888',

        # Validation toolbar.
        Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',

        # Status toolbar.
        Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',
        Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',
        Token.Toolbar.Status.Off:                     'bg:#222222 #888888',
        Token.Toolbar.Status.On:                      'bg:#222222 #ffffff',
        Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',

        # Completer toolbar.
        Token.Toolbar.Completions:                    'noinherit',
        Token.Toolbar.Completions.Arrow:              'bold #888888',
        Token.Toolbar.Completions.Completion:         '#888888 noinherit',
        Token.Toolbar.Completions.Completion.Current: 'bold noinherit',

        # Completer menu.
        Token.Menu.Completions.Completion:            'bg:#888888 #ffffbb',
        Token.Menu.Completions.Completion.Current:    'bg:#dddddd #000000',
        Token.Menu.Completions.Meta:                  'bg:#888888 #cccccc',
        Token.Menu.Completions.Meta.Current:          'bg:#bbbbbb #000000',
        Token.Menu.Completions.ProgressBar:           'bg:#aaaaaa',
        Token.Menu.Completions.ProgressButton:        'bg:#000000',

        # When Control-C has been pressed. Grayed.
        Token.Aborted:                                '#888888',

        # Vi-style tildes.
        Token.Leftmargin.Tilde:                       '#888888',
    }

