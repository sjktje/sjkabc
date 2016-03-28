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
from pytest import fixture, raises
from sjkabc import Tune
from sjkabc.sjkabc import HEADER_KEYS

from tests.factories import TuneFactory

@fixture
def tune_object():
        return TuneFactory()

def test_expanded_abc_returns_expanded_abc(tune_object):
    assert tune_object.expanded_abc == 'aaabbbcccaaabbbccc'


def test_tune_string_representation(tune_object):
    assert str(tune_object) == 'Test tune'


def test_get_header_line(tune_object):
    titles = [title for title in tune_object._get_header_line('title')]
    assert titles == ['T:Test tune']


def test_tune_initialises_empty_lists():
    t = Tune()
    for key in HEADER_KEYS:
        assert getattr(t, HEADER_KEYS[key]) == []

    for attr in ['abc', '_expanded_abc']:
        assert getattr(t, attr) == []


def test_format_abc_does_not_include_empty_info_fields(tune_object):
    INFOLINE_REGEXP = re.compile(r'[BCDFGHIKLMNOPQRSTXZ]{1}:(.*)')

    for line in tune_object.format_abc().splitlines():
        if INFOLINE_REGEXP.match(line):
            assert len(line) > 2


def test_cannot_set_incorrect_attribute_through_init():
    t = Tune(something_incorrect='testing')
    with raises(AttributeError):
        t.something_incorrect

if __name__ == "__main__":
    pytest.main()
