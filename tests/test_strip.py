#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test_strip
    ~~~~~~~~~~

    Tests for the strip_* functions.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""


import pytest

from sjkabc.sjkabc import strip_whitespace, strip_accidentals, strip_octave, \
    strip_bar_dividers, strip_triplets, strip_chords, strip_extra_chars, \
    strip_gracenotes, strip_decorations, strip_ornaments, strip_slurs


def test_strip_whitespace():
    abc = 'abcd efga|dega\r bega\n|{/d}ABcd BEGA'
    should_be = 'abcdefga|degabega|{/d}ABcdBEGA'
    assert strip_whitespace(abc) == should_be


def test_strip_accidentals():
    abc = 'AB^cd e=fga|_abcd =abcd'
    should_be = 'ABcd efga|abcd abcd'
    assert strip_accidentals(abc) == should_be


def test_strip_ornaments_strips_gracenotes():
    abc = 'abc{/d}|ab{cd}ef'
    should_be = 'abc|abef'
    assert strip_ornaments(abc) == should_be


def test_strip_ornaments_strips_trills():
    abc = 'abc!trill(!d ef!trill)!gh'
    should_be = 'abcd efgh'
    assert strip_ornaments(abc) == should_be


def test_strip_ornaments_strips_turns():
    abc = 'abc!turn!d ef!turn!gh'
    should_be = 'abcd efgh'
    assert strip_ornaments(abc) == should_be


def test_strip_ornaments_strips_fermatas():
    abc = 'ab!fermata!cd efgh!fermata!'
    should_be = 'abcd efgh'
    assert strip_ornaments(abc) == should_be


def test_strip_octave():
    abc = "A,B,CDEFGABcdefgabc'd'e'f'g'a'"
    should_be = 'ABCDEFGABcdefgabcdefga'
    assert strip_octave(abc) == should_be


def test_strip_bar_dividers():
    abc = 'abcd abcd|baga BAGA|{/ba}baga DAGA|'
    should_be = 'abcd abcdbaga BAGA{/ba}baga DAGA'
    assert strip_bar_dividers(abc) == should_be


def test_strip_bar_dividers_doesnt_strip_repeats():
    abc = 'aaa|bbb|ccc|ddd:|'
    should_be = 'aaabbbcccddd:|'
    assert strip_bar_dividers(abc) == should_be


def test_strip_bar_dividers_removes_end_char():
    abc = 'aaa|bbb|ccc|ddd|]'
    should_be = 'aaabbbcccddd'
    assert strip_bar_dividers(abc) == should_be


def test_strip_triplets():
    abc = 'abc (3bbb|bab (3abc|(3GDF bab'
    should_be = 'abc bbb|bab abc|GDF bab'
    assert strip_triplets(abc) == should_be


def test_strip_chords():
    abc = '"Gm" GABd|[C,c]def'
    should_be = ' GABd|def'
    assert strip_chords(abc) == should_be


def test_strip_extra_chards():
    abc = 'A/B/c e<cd>|cBAF ABce\\|dBGA BdcB'
    should_be = 'ABc ecd|cBAF ABce|dBGA BdcB'
    assert strip_extra_chars(abc) == should_be


def test_strip_gracenotes():
    abc = "ABcd {/d}Bcde|B{/d}B{/A}B e {/dada}eAce|BAGA {dega}BAGA"
    should_be = "ABcd Bcde|BBB e eAce|BAGA BAGA"
    assert strip_gracenotes(abc) == should_be


def test_strip_slurs():
    abc = "ABCD (abcd)|ab(cd) (a)BCd|(abcd abcd):|"
    should_be = "ABCD abcd|abcd aBCd|abcd abcd:|"
    assert strip_slurs(abc) == should_be


class TestDecorations():
    def test_strip_staccatos(self):
        abc = '|:a.b.c.:|'
        assert strip_decorations(abc) == '|:abc:|'

    def test_strip_rolls(self):
        abc = '|:a~b~cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_fermatas(self):
        abc = '|:aHbcd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_accent_or_emphasis(self):
        abc = '|:aLbLcd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_lowermordent(self):
        abc = '|:aMbMcMd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_codas(self):
        abc = '|:aObOcd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_uppermordent(self):
        abc = '|:aPbPcPd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_segno(self):
        abc = '|:aSbScSd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_trill(self):
        abc = '|:aTbTcTd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_upbow(self):
        abc = '|:aubucud:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shorthand_downbow(self):
        abc = '|:avbvcvd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_trills(self):
        abc = '|:ab!trill!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_start_of_extended_trill(self):
        abc = '|:ab!trill(!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_end_of_extended_trill(self):
        abc = '|:ab!trill)!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_lowermordent(self):
        abc = '|:ab!lowermordent!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_uppermordent(self):
        abc = '|:ab!uppermordent!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_mordent(self):
        abc = '|:ab!mordent!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_pralltriller(self):
        abc = '|:ab!pralltriller!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_roll(self):
        abc = '|:ab!roll!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_turn(self):
        abc = '|:ab!turn!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_turnx(self):
        abc = '|:ab!turnx!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_invertedturn(self):
        abc = '|:ab!invertedturn!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_invertedturnx(self):
        abc = '|:ab!invertedturnx!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_arpeggio(self):
        abc = '|:ab!arpeggio!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_greater_than_mark(self):
        abc = '|:ab!>!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_accent(self):
        abc = '|:ab!accent!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_emphasis(self):
        abc = '|:ab!emphasis!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_fermata(self):
        abc = '|:ab!fermata!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_invertedfermata(self):
        abc = '|:ab!invertedfermata!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_tenuto(self):
        abc = '|:ab!tenuto!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_fingerings(self):
        for i in range(6):
            abc = '|:ab!{}!cd:|'.format(i)
            assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_left_hand_pizzicato(self):
        abc = '|:ab!+!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

        abc = '|:ab!plus!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_snap(self):
        abc = '|:ab!snap!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_slide(self):
        abc = '|:ab!slide!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_wedge(self):
        abc = '|:ab!wedge!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_upbow(self):
        abc = '|:ab!upbow!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_downbow(self):
        abc = '|:ab!downbow!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_open(self):
        abc = '|:ab!open!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_thumb(self):
        abc = '|:ab!thumb!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_breath(self):
        abc = '|:ab!breath!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_dynamic_marks(self):
        for mark in ['pppp', 'ppp', 'pp', 'p', 'mp', 'mf',
                     'f', 'ff', 'fff', 'ffff', 'sfz']:
            abc = '|:ab!{}!cd:|'.format(mark)
            assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_crescendos(self):
        for mark in ['crescendo(', '<(', 'crescendo)', '<)']:
            abc = '|:ab!{}!cd:|'.format(mark)
            assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_diminuendos(self):
        for mark in ['diminuendo(', '>(', 'diminuendo)', '>)']:
            abc = '|:ab!{}!cd:|'.format(mark)
            assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_segno(self):
        abc = '|:ab!segno!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_coda(self):
        abc = '|:ab!coda!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_ds(self):
        abc = '|:ab!D.S.!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_dc(self):
        abc = '|:ab!D.C.!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_dacapo(self):
        abc = '|:ab!dacapo!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_dacoda(self):
        abc = '|:ab!dacoda!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_fine(self):
        abc = '|:ab!fine!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_shortphrase(self):
        abc = '|:ab!shortphrase!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_mediumphrase(self):
        abc = '|:ab!mediumphrase!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'

    def test_strip_longphrase(self):
        abc = '|:ab!longphrase!cd:|'
        assert strip_decorations(abc) == '|:abcd:|'


if __name__ == "__main__":
    pytest.main()
