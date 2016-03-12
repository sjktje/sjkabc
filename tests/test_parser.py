#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test_parser
    ~~~~~~~~~~~

    This module contains tests for the Parser class.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""


import pytest
from pytest import fixture

from sjkabc import Parser


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


def test_line_is_continued_line():
    p = Parser()
    assert p._line_is_continued_line('+:something')


def test_line_is_not_continued_line():
    p = Parser()
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


if __name__ == "__main__":
    pytest.main()
