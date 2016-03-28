#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test_header_keys
    ~~~~~~~~~~~~~~~~

    The HEADER_KEYS dictionary contains the ABC header fields supported by
    sjkabc.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""


import pytest
from pytest import raises

from sjkabc.sjkabc import get_id_from_field, get_field_from_id


def test_get_id_from_field_returns_correct_id():
    assert get_id_from_field('title') == 'T'


def test_get_id_from_field_raises_keyerror():
    with raises(KeyError):
        get_id_from_field('baba')


def test_get_field_from_id_returns_correct_field():
    assert get_field_from_id('T') == 'title'


def test_get_field_from_id_raises_keyerror():
    with raises(KeyError):
        get_field_from_id('/')


if __name__ == "__main__":
    pytest.main()
