#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test_tune
    ~~~~~~~~~

    Tests for the Tune class.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""


import re
import pytest
from pytest import fixture

from sjkabc import Tune
from sjkabc.sjkabc import HEADER_KEYS


def test_expanded_abc_returns_expanded_abc():
    t = Tune()
    t.abc = '|:abc abc|bcd bcd:|'
    should_be = 'abcabcbcdbcdabcabcbcdbcd'
    assert t.expanded_abc == should_be


def test_tune_string_representation():
    t = Tune()
    t.title.append('Test')
    assert str(t) == 'Test'


@fixture
def tune_object():
    t = Tune()
    t.book.append('The Bible')
    t.composer.append('John Doe')
    t.discography.append('Best hits')
    t.file.append('http://bogus.url.com/test.abc')
    t.group.append('Test')
    t.history.append('Interesting')
    t.instruction.append('Some instructions')
    t.key.append('Gm')
    t.note_length.append('1/8')
    t.metre.append('4/4')
    t.notes.append('A note')
    t.origin.append('Sweden')
    t.parts.append('AABB')
    t.tempo.append('108')
    t.rhythm.append('reel')
    t.source.append('John Smith')
    t.title.append('Test title')
    t.title.append('Second test title')
    t.index.append('1')
    t.transcription.append('Doctor Who')
    t.abc.append('|:aaa|bbb|ccc:|')
    return t


def test_get_header_line(tune_object):
    titles = [title for title in tune_object._get_header_line('title')]
    assert titles == ['T:Test title', 'T:Second test title']


def test_format_abc_returns_header_lines_in_correct_order(tune_object):
    should_be = """X:1
T:Test title
T:Second test title
C:John Doe
O:Sweden
R:reel
B:The Bible
D:Best hits
F:http://bogus.url.com/test.abc
G:Test
H:Interesting
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

    assert tune_object.format_abc() == should_be


def test_tune_object_initialises_empty_lists():
    t = Tune()
    for key in HEADER_KEYS:
        assert getattr(t, HEADER_KEYS[key]) == []

    for attr in ['abc', '_expanded_abc']:
        assert getattr(t, attr) == []


def test_format_abc_does_not_include_empty_info_fields(tune_object):
    tune_object.history.append('')
    INFOLINE_REGEXP = re.compile(r'[BCDFGHIKLMNOPQRSTXZ]{1}:(.*)')

    for line in tune_object.format_abc().splitlines():
        if INFOLINE_REGEXP.match(line):
            assert len(line) > 2


if __name__ == "__main__":
    pytest.main()
