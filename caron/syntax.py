# -*- coding: utf-8 -*-


import sys
import collections
import re
import os

import functools

import utility


indent = 0
output = sys.stdout

re_indent = re.compile(r'^(( |\t)*)', re.MULTILINE)

myglobals = dict()


def add_indent(string):
    return re.sub(re_indent, ' ' * (indent * 2), string)


def is_iterable(it):
    return not isinstance(it, str) and isinstance(it, collections.Iterable)


def join_if_iterable(s, it):
    if is_iterable(it):
        return s.join(it)
    else:
        return it


def write_indent():
    output.write(' ' * (indent * 2))


class Item(object):
    def __iadd__(self, c):
        write_indent()
        output.write('\\item')

        if not isinstance(c, str) and '__getitem__' in dir(c):
            output.write('[')
            output.write(join_if_iterable(',', c[0]))
            output.write(']')
            _item = c[1]
        else:
            _item = c

        output.write(' ')
        output.write(join_if_iterable(',', _item))
        output.write('\n')

        return self


def make_title():
    write_indent()
    output.write('\\maketitle\n')


def centering():
    write_indent()
    output.write('\\centering\n')


def include_graphics(options, filename):
    write_indent()
    output.write('\\includegraphics[')
    output.write(join_if_iterable(',', options))
    output.write(']{')
    output.write(filename)
    output.write('}\n')


def caption(content, label=None, type=None):
    write_indent()
    if type is None:
        output.write('\\caption{')
    elif type == 'figure':
        output.write('\\figcaption{')
    elif type == 'table':
        output.write('\\tblcaption{')
    else:
        raise RuntimeError('unknown caption type')
    output.write(content)
    output.write('}\n')
    if label is not None:
        write_indent()
        output.write('\\label{')
        output.write(label)
        output.write('}\n')


class Line(object):
    def __iadd__(self, s):
        s = add_indent(s)
        if len(s) == 0:
            output.write('\n')
        else:
            output.write(s)
            if s[-1] != '\n':
                output.write('\n')
        return self


    def __call__(self, s):
        self.__iadd__(s)


class Raw(object):
    def __iadd__(self, s):
        if len(s) == 0:
            output.write('\n')
        else:
            output.write(s)
            if s[-1] != '\n':
                output.write('\n')
        return self


    def __call__(self, s):
        self.__iadd__(s)


item = Item()
line = Line()
raw = Raw()


class Document(object):
    def __enter__(self):
        output.write(r"""\documentclass[a4paper]{bxjsarticle}
\usepackage{zxjatype}

\usepackage{xltxtra}
\setmainfont{Palatino Linotype}
\setjamainfont{IPAMincho}
\setsansfont{IPAPGothic}
\setjasansfont{IPAPGothic}
\setmonofont{IPAGothic}
\setjamonofont{IPAGothic}
\XeTeXlinebreaklocale "ja"

%\def\baselinestretch{1.2}
\setlength{\paperwidth}{210mm}
\setlength{\paperheight}{297mm}
\setlength{\oddsidemargin}{0mm}
\setlength{\evensidemargin}{0mm}
\setlength{\topmargin}{0mm}
\setlength{\headheight}{0mm}
\setlength{\headsep}{0mm}
\setlength{\footskip}{13mm}
\setlength{\textheight}{247.6mm}
\setlength{\textwidth}{159.2mm}

\usepackage{url}
\usepackage{graphicx}
\usepackage{color}
\usepackage{bxascmac}

\usepackage{framed}
\usepackage{fancyvrb}

\makeatletter
\def\PY@reset{\let\PY@it=\relax \let\PY@bf=\relax%
    \let\PY@ul=\relax \let\PY@tc=\relax%
    \let\PY@bc=\relax \let\PY@ff=\relax}
\def\PY@tok#1{\csname PY@tok@#1\endcsname}
\def\PY@toks#1+{\ifx\relax#1\empty\else%
    \PY@tok{#1}\expandafter\PY@toks\fi}
\def\PY@do#1{\PY@bc{\PY@tc{\PY@ul{%
    \PY@it{\PY@bf{\PY@ff{#1}}}}}}}
\def\PY#1#2{\PY@reset\PY@toks#1+\relax+\PY@do{#2}}

\expandafter\def\csname PY@tok@se\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.73,0.40,0.13}{##1}}}
\expandafter\def\csname PY@tok@sx\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@il\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@k\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@mi\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@w\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.73,0.73}{##1}}}
\expandafter\def\csname PY@tok@nt\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@gu\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.50,0.00,0.50}{##1}}}
\expandafter\def\csname PY@tok@nn\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,1.00}{##1}}}
\expandafter\def\csname PY@tok@kn\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@na\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.49,0.56,0.16}{##1}}}
\expandafter\def\csname PY@tok@mf\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@ni\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.60,0.60,0.60}{##1}}}
\expandafter\def\csname PY@tok@kt\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.69,0.00,0.25}{##1}}}
\expandafter\def\csname PY@tok@s1\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
\expandafter\def\csname PY@tok@gd\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.63,0.00,0.00}{##1}}}
\expandafter\def\csname PY@tok@ge\endcsname{\let\PY@it=\textit}
\expandafter\def\csname PY@tok@c1\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
\expandafter\def\csname PY@tok@kr\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@cp\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.74,0.48,0.00}{##1}}}
\expandafter\def\csname PY@tok@o\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@gh\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,0.50}{##1}}}
\expandafter\def\csname PY@tok@nv\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
\expandafter\def\csname PY@tok@mh\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@s\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
\expandafter\def\csname PY@tok@sb\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
\expandafter\def\csname PY@tok@s2\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
\expandafter\def\csname PY@tok@gp\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,0.50}{##1}}}
\expandafter\def\csname PY@tok@no\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.53,0.00,0.00}{##1}}}
\expandafter\def\csname PY@tok@si\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.73,0.40,0.53}{##1}}}
\expandafter\def\csname PY@tok@sc\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
\expandafter\def\csname PY@tok@kp\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@vi\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
\expandafter\def\csname PY@tok@kc\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@kd\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@gs\endcsname{\let\PY@bf=\textbf}
\expandafter\def\csname PY@tok@sr\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.40,0.53}{##1}}}
\expandafter\def\csname PY@tok@vg\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
\expandafter\def\csname PY@tok@nf\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,1.00}{##1}}}
\expandafter\def\csname PY@tok@mo\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@cm\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
\expandafter\def\csname PY@tok@nb\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@sh\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
\expandafter\def\csname PY@tok@ss\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
\expandafter\def\csname PY@tok@mb\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@err\endcsname{\def\PY@bc##1{\setlength{\fboxsep}{0pt}\fcolorbox[rgb]{1.00,0.00,0.00}{1,1,1}{\strut ##1}}}
\expandafter\def\csname PY@tok@ow\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.67,0.13,1.00}{##1}}}
\expandafter\def\csname PY@tok@gt\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.27,0.87}{##1}}}
\expandafter\def\csname PY@tok@nd\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.67,0.13,1.00}{##1}}}
\expandafter\def\csname PY@tok@vc\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
\expandafter\def\csname PY@tok@ne\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.82,0.25,0.23}{##1}}}
\expandafter\def\csname PY@tok@nl\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.63,0.63,0.00}{##1}}}
\expandafter\def\csname PY@tok@sd\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
\expandafter\def\csname PY@tok@go\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.53,0.53,0.53}{##1}}}
\expandafter\def\csname PY@tok@bp\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
\expandafter\def\csname PY@tok@cs\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
\expandafter\def\csname PY@tok@gr\endcsname{\def\PY@tc##1{\textcolor[rgb]{1.00,0.00,0.00}{##1}}}
\expandafter\def\csname PY@tok@m\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
\expandafter\def\csname PY@tok@gi\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.63,0.00}{##1}}}
\expandafter\def\csname PY@tok@c\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
\expandafter\def\csname PY@tok@nc\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,1.00}{##1}}}

\def\PYZbs{\char`\\}
\def\PYZus{\char`\_}
\def\PYZob{\char`\{}
\def\PYZcb{\char`\}}
\def\PYZca{\char`\^}
\def\PYZam{\char`\&}
\def\PYZlt{\char`\<}
\def\PYZgt{\char`\>}
\def\PYZsh{\char`\#}
\def\PYZpc{\char`\%}
\def\PYZdl{\char`\$}
\def\PYZhy{\char`\-}
\def\PYZsq{\char`\'}
\def\PYZdq{\char`\"}
\def\PYZti{\char`\~}
% for compatibility with earlier versions
\def\PYZat{@}
\def\PYZlb{[}
\def\PYZrb{]}

\newcommand{\figcaption}[1]{\def\@captype{figure}\caption{#1}}
\newcommand{\tblcaption}[1]{\def\@captype{table}\caption{#1}}

\def\sourcecodecaption{ソースコード}

\newcounter{caronsourcecodecounter}
\setcounter{caronsourcecodecounter}{0}

\newenvironment{caronsourcecode}[2][]{
\begin{center}
\refstepcounter{caronsourcecodecounter}#1
%\vspace{-1.5em}
}{
\end{center}
}
\makeatother
""")

        if 'preamble' in myglobals:
            preamble = myglobals['preamble']
            if 'package' in preamble:
                package = preamble['package']
                if isinstance(package, str):
                    output.write(r'\usepackage{' + package + '}\n')
                elif isinstance(package, tuple) or isinstance(package, list):
                    for p in package:
                        if isinstance(p, str):
                            output.write(r'\usepackage{' + p + '}\n')
                        elif isinstance(p, tuple) or isinstance(p, list):
                            output.write(r'\usepackage[')
                            output.write(join_if_iterable(',', p[0]))
                            output.write(']{')
                            output.write(join_if_iterable(',', p[1]))
                            output.write('}\n')
                output.write('\n')
            if 'title' in preamble:
                output.write('\n\\title{')
                output.write(preamble['title'])
                output.write('}\n')
            if 'author' in preamble:
                output.write('\\author{')
                output.write(preamble['author'])
                output.write('}\n')
            if 'date' in preamble:
                output.write('\\date{')
                output.write(preamble['date'])
                output.write('}\n')
            if 'raw' in preamble:
                output.write('\n')
                output.write(preamble['raw'])
                output.write('\n')

        output.write('\n\\begin{document}\n')


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            output.write('\\end{document}\n')


class SectionBase(object):
    def __init__(self, command, title):
        self.command = command
        self.title = title


    def __enter__(self):
        output.write('\\{0}{{{1}}}\n'.format(self.command, self.title))


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            output.write('\n')


class SourceCode(object):
    def __init__(self, filename, caption=None, language=None, label=None, encoding=None):
        if caption is None:
            caption = filename
        if language is None:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ('.cpp', '.hpp'):
                language = 'c++'
            elif ext in ('.c', '.h'):
                language = 'c'
            elif ext == '.py':
                language = 'python'
            elif ext == '.rb':
                language = 'ruby'
            elif ext == '.js':
                language = 'javascript'
        if encoding is None:
            encoding = utility.get_encoding(filename, None)

        self.filename = filename
        self.caption = caption
        self.language = language
        self.encoding = encoding
        self.label = label


    def __enter__(self):
        write_indent()
        output.write('\\begin{caronsourcecode}')

        if self.label is not None:
            output.write('[\label{')
            output.write(self.label)
            output.write('}]')

        output.write('{')
        output.write(self.caption)
        output.write('}\n')

        content = open(self.filename, encoding=self.encoding).read()

        if content.startswith('\ufeff'):
            content = content[1:]

        output.write(utility.syntax_highlight(content, self.language).replace(
            'commandchars',
            r'frame=single,'
            r'fontsize=\small,'
            r'label=\textrm{{\sourcecodecaption\thecaronsourcecodecounter\ \ {0}}},'
            r'commandchars'.format(self.caption)
        ))


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            write_indent()
            output.write('\\end{caronsourcecode}\n')


class Equation(object):
    def __enter__(self):
        write_indent()
        output.write('\\[\n')


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            write_indent()
            output.write('\\]\n')


class Environment(object):
    def __init__(self, name, optional=None, required=None):
        self.begin = '\\begin{' + name + '}'
        self.end = '\\end{' + name + '}\n'

        if optional is not None:
            self.begin += '[' + join_if_iterable(',', optional) + ']'
        if required is not None:
            self.begin += '{' + join_if_iterable(',', required) + '}'

        self.begin += '\n'


    def __enter__(self):
        write_indent()
        output.write(self.begin)

        global indent
        indent += 1


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            global indent
            indent -= 1
            write_indent()

            output.write(self.end)


Section = functools.partial(SectionBase, 'section')
SubSection = functools.partial(SectionBase, 'subsection')
SubSubSection = functools.partial(SectionBase, 'subsubsection')
Paragraph = functools.partial(SectionBase, 'paragraph')


Itemize = functools.partial(Environment, 'itemize')
Enumerate = functools.partial(Environment, 'enumerate')
Table = functools.partial(Environment, 'table')
Tabular = functools.partial(Environment, 'tabular')