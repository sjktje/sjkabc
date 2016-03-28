#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test_expand
    ~~~~~~~~~~~

    Testing module for expand_* functions.

    The expand functions are used to convert ABC notation into a string that
    is suitable for searching.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""


import pytest
import re

from sjkabc.sjkabc import expand_notes, expand_parts, expand_abc


def test_expand_notes():
    abc = 'G3 EGD|G3 EGD|G2G BGB|d3 BAB'
    should_be = 'GGG EGD|GGG EGD|GGG BGB|ddd BAB'
    assert expand_notes(abc) == should_be


def test_expand_lone_end_repeat():
    abc = 'abc abc|bcd bcd|cde cde|def def:|'
    should_be = 'abc abc|bcd bcd|cde cde|def def|' + \
                'abc abc|bcd bcd|cde cde|def def|'
    assert expand_parts(abc) == should_be


def test_expand_start_and_end_repeat():
    abc = '|:abc abc|bcd bcd|cde cde|def def:|'
    should_be = 'abc abc|bcd bcd|cde cde|def def|' + \
                'abc abc|bcd bcd|cde cde|def def|'
    assert expand_parts(abc) == should_be


def test_expand_two_repeats_first_being_lone():
    abc = 'abc abc|bcd bcd|cde cde|def def:|' + \
          '|:bcd bcd|cde cde|def def|efg efg:|'
    should_be = 'abc abc|bcd bcd|cde cde|def def|' + \
                'abc abc|bcd bcd|cde cde|def def|' + \
                'bcd bcd|cde cde|def def|efg efg|' + \
                'bcd bcd|cde cde|def def|efg efg|'
    assert expand_parts(abc) == should_be


def test_expand_two_repeats():
    abc = '|:abc abc|bcd bcd|cde cde|def def:|' + \
          '|:bcd bcd|cde cde|def def|efg efg:|'
    should_be = 'abc abc|bcd bcd|cde cde|def def|' + \
                'abc abc|bcd bcd|cde cde|def def|' + \
                'bcd bcd|cde cde|def def|efg efg|' + \
                'bcd bcd|cde cde|def def|efg efg|'
    assert expand_parts(abc) == should_be


def test_expand_two_repeats_with_double_colon_syntax():
    abc = '|:aaa|bbb::' + \
          'ccc|ddd:|'
    should_be = 'aaa|bbb|aaa|bbb|ccc|ddd|ccc|ddd|'
    assert expand_parts(abc) == should_be


def test_expand_part_with_two_one_bar_endings():
    abc = 'abc bcd|abc bcd|1deg bag:|2geg gag||'
    should_be = 'abc bcd|abc bcd|deg bag|' + \
                'abc bcd|abc bcd|geg gag|'
    assert expand_parts(abc) == should_be


def test_expand_part_with_two_one_bar_endings_with_start_repeat():
    abc = '|:abc bcd|abc bcd|1deg bag:|2geg gag||'
    should_be = 'abc bcd|abc bcd|deg bag|' + \
                'abc bcd|abc bcd|geg gag|'
    assert expand_parts(abc) == should_be


def test_expand_part_with_two_two_bar_endings():
    abc = 'abc bcd|abc bcd|1deg bag|eae eae:|2geg gag|gbg gbg||'
    should_be = 'abc bcd|abc bcd|deg bag|eae eae|' + \
                'abc bcd|abc bcd|geg gag|gbg gbg|'
    assert expand_parts(abc) == should_be


def test_expand_part_with_two_two_bar_endings_with_start_repeat():
    abc = '|:abc bcd|abc bcd|1deg bag|eae eae:|2geg gag|gbg gbg||'
    should_be = 'abc bcd|abc bcd|deg bag|eae eae|' + \
                'abc bcd|abc bcd|geg gag|gbg gbg|'
    assert expand_parts(abc) == should_be


def test_expand_two_part_tune_with_two_one_bar_endings():
    abc = 'ceec defd|ceaf ecAB|ceec defd|1ceBe cAAB:|2ceBe cAAc||' + \
          '|:eaae fgaf|e/e/e ef ecAc|eaae fgaf|1ecBe cAAc:|2ecBe cAAB|]'
    should_be = 'ceec defd|ceaf ecAB|ceec defd|ceBe cAAB|' + \
                'ceec defd|ceaf ecAB|ceec defd|ceBe cAAc|' + \
                'eaae fgaf|e/e/e ef ecAc|eaae fgaf|ecBe cAAc|' + \
                'eaae fgaf|e/e/e ef ecAc|eaae fgaf|ecBe cAAB|'
    assert expand_parts(abc) == should_be


def test_expand_three_part_tune():
    abc = 'B3B {/d}BAGA|B2GB AGEG|DBB/B/B BAGB|A/B/cBG AGEG|' \
          'B3 B2 A GA|B2GB AGEG|Beed BedB|AdBG A/B/AGE||' \
          '|:DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc' \
          '|1dBAc BGGE:|2dBAc BGBc||' \
          '|:d2Bd egge|dB~B2 ABGB|d2Bd egge|1agbg ageg:|2agbg aged|]'
    should_be = 'B3B {/d}BAGA|B2GB AGEG|DBB/B/B BAGB|A/B/cBG AGEG|' + \
                'B3 B2 A GA|B2GB AGEG|Beed BedB|AdBG A/B/AGE|' + \
                'DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc|dBAc BGGE|' + \
                'DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc|dBAc BGBc|' + \
                'd2Bd egge|dB~B2 ABGB|d2Bd egge|agbg ageg|' + \
                'd2Bd egge|dB~B2 ABGB|d2Bd egge|agbg aged|'
    assert expand_parts(abc) == should_be


def test_expand_abc():
    abc = 'A2eA BAec|ABcd egdB|G2dG BGdG|G/G/G dG BAGB|\\' + \
          'A2eA BAec|ABcd egdB|GABd eaaf|1gedB BAAG:|2gedB BAce||' + \
          '|:a2ea ageg|agbg agea|gedc BGBd|~g3a bgeg|\n' + \
          'a2ea ageg|agbg ageg|~d3e ~g3e|1dBGB BAce:|2dBGB BAAG|]'
    should_be = 'aaeabaecabcdegdbggdgbgdggggdgbagb' + \
                'aaeabaecabcdegdbgabdeaafgedbbaag' + \
                'aaeabaecabcdegdbggdgbgdggggdgbagb' + \
                'aaeabaecabcdegdbgabdeaafgedbbace' + \
                'aaeaagegagbgageagedcbgbdgggabgeg' + \
                'aaeaagegagbgagegdddegggedbgbbace' + \
                'aaeaagegagbgageagedcbgbdgggabgeg' + \
                'aaeaagegagbgagegdddegggedbgbbaag'
    assert expand_abc(abc) == should_be


def test_expanded_string_should_only_contain_lowercase_letters_a_to_g_and_z():
    TUNE_BODY_REGEXP = re.compile(r'^[a-gz]*$')
    abc = """
    A/B/c e<cd>|cBAF gbdA|(ab)cd !trill!baba|z deg z deg:|
    |:ba{/b}b ba{bbb}ba|gaGC GefD|1"chord"[M:4/4]abab gGGG:|2egag gaGG|]
    """
    expanded = expand_abc(abc)
    assert TUNE_BODY_REGEXP.match(expanded)

if __name__ == "__main__":
    pytest.main()
