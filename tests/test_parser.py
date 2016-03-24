#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test_parser
    ~~~~~~~~~~~

    This module contains tests for the Parser class and the parse_ functions.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""


import pytest
from pytest import fixture

from sjkabc import Parser, parse_dir, parse_file

@fixture
def tune1():
    abc = """X:1
T: In Memory Of Coleman
C: Ed Reavy
R: Reel
O: Ireland
M: 4/4
H: So here's the story. And it
+: continues on this line.
H: Another anecdote without continuation.
L: 1/8
Z: Svante Kvarnström
P: AB
K: Gm
[P: A]DGBd cBGF|DF~F2 GFDF|GABc dgga|b/a/gaf dgga|
(ab)ag gfdc|B/c/dBG FDCF|DGBd c2Bc|1dgdc BGGF:|2dgdc BGGA||
[P: B]|:(AB)Bd g3f|=ec~c2 AF~F2|G z g=e fdcA|FAcA BGGA|
(AB)fB DBfB|DBfB AF~F2|G3B dBcA|1B/c/dcA G3A:|2B/c/dcA G3F|]
"""
    return abc


@fixture
def tune2():
    abc = """X:37
T:Apples In Winter
T:Fictional second name
T:Fictional third name
C:Trad.
R:Jig
M:6/8
L:1/8
Z:Svante Kvarnström
K:Em
BEE BEE|Bdf edB|BAF FEF|DFA BAF|
BEE BEE|Bdf edB|BAB dAF|1FED EGA:|2FED EAc||
|:e2f gfe|eae edB|BAF FEF|DFA BAF|
e2f gfe|eae edB|BAB dAF|1FED EAc:|2FED E3|]
"""
    return abc


@fixture
def two_abc_tunes(tune1, tune2):
    return tune1 + tune2


@fixture
def p_tune():
    abc = """X:1
T:Test title
T:Second test title
C:John Doe
O:Sweden
R:reel
B:The Bible
D:Best hits
F:http://bogus.url.com/test.abc
G:Test
H:Interesting history
+:about something.
H:And here is
+:another one.
N:A note
S:John Smith
Z:Doctor Who
P:AABB
M:4/4
L:1/8
Q:108
K:Gm
|:aaa|bbb|ccc:|
"""

    tune = [tune for tune in Parser(abc)][-1]
    return tune


@fixture
def p():
    return Parser()


def test_line_is_continued_line(p):
    assert p._line_is_continued_line('+:something')


def test_line_is_not_continued_line(p):
    assert not p._line_is_continued_line('C:composer info')


def test_line_is_key(p):
    assert p._line_is_key('K:Gm')


def test_line_is_not_key(p):
    assert not p._line_is_key('Z:John Doe')


def test_line_is_empty(p):
    assert p._line_empty('')
    assert p._line_empty('    ')


def test_line_is_not_empty(p):
    assert not p._line_empty('D:Greatest hits')


def test_line_is_comment(p):
    assert p._line_comment('% This is a test')


def test_line_is_not_a_comment(p):
    assert not p._line_comment('O:Sweden')


def test_line_is_index(p):
    assert p._line_is_index('X:1029')


def test_line_is_not_index(p):
    assert not p._line_is_index('S:John Smith')


def test_continued_history_line_is_parsed_correctly(p_tune):
    should_be = ['Interesting history about something.',
                 'And here is another one.']

    assert p_tune.history == should_be


def test_parsed_info_line_should_not_start_with_space(tune1):
    tunes = [t for t in Parser(tune1)]
    assert not tunes[0].history[0].startswith(' ')


def test_parse_file(tmpdir, two_abc_tunes):
    f = tmpdir.join('tunes.abc')
    f.write(two_abc_tunes)
    tunes = [tune for tune in parse_file(str(f))]
    indexes = [i.index for i in tunes]

    assert len(tunes) == 2

    assert ['1'] in indexes
    assert ['37'] in indexes


def test_parse_dir(tmpdir, tune1, tune2):
    d = tmpdir.mkdir('tunes')

    d.join('tune1.abc').write(tune1)
    d.join('tune2.abc').write(tune2)

    tunes = [t for t in parse_dir(str(d))]
    indexes = [i.index for i in tunes]

    assert ['1'] in indexes
    assert ['37'] in indexes


if __name__ == "__main__":
    pytest.main()
