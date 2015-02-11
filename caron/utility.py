# -*- coding: shift_jis -*-


import cchardet
import pygments
import pygments.lexers
import pygments.lexers.c_cpp
import pygments.lexers.ruby
import pygments.lexers.javascript
import pygments.lexers.dotnet
import pygments.formatters


def get_encoding(filename, encoding):
    if encoding is None:
        encoding = cchardet.detect(open(filename, 'rb').read())['encoding']
    return encoding


def syntax_highlight(code, language):
    language = language.lower()
    if language == 'c++':
        lexer = pygments.lexers.c_cpp.CppLexer
    elif language == 'c':
        lexer = pygments.lexers.c_cpp.CLexer
    elif language == 'python':
        lexer = pygments.lexers.PythonLexer
    elif language == 'ruby':
        lexer = pygments.lexers.ruby.Lexer
    elif language == 'javascript':
        lexer = pygments.lexers.javascript.JavascriptLexer
    elif language == 'csharp':
        lexer = pygments.lexers.dotnet.CSharpLexer

    return pygments.highlight(code, lexer(), pygments.formatters.LatexFormatter())