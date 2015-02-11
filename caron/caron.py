# -*- coding: utf-8 -*-


import os

import sys
import argparse

import syntax
import utility


def get_destination_name(filename):
    return os.path.splitext(filename)[0] + '.tex'


def execute(filename, encoding=None):
    dest = get_destination_name(filename)
    encoding = utility.get_encoding(filename, encoding)

    code = compile(open(filename, encoding=encoding).read(), filename, 'exec')

    syntax.myglobals = globals()
    syntax.myglobals.update({i: syntax.__getattribute__(i)
                      for i in dir(syntax) if i[0].isupper()})
    syntax.myglobals.update({
        'make_title': syntax.make_title,
        'centering': syntax.centering,
        'include_graphics': syntax.include_graphics,
        'caption': syntax.caption,
        'item': syntax.item,
        'line': syntax.line,
        'raw': syntax.raw,
        'indent': syntax.add_indent,
        'newline': r'\\',
    })

    syntax.output = open(dest, 'w', encoding='utf-8')

    exec(code, syntax.myglobals)


if __name__ == '__main__':
    execute(sys.argv[1])