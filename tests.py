#!/usr/bin/env python
# encoding: utf-8

import unittest
from sjkabc.sjkabc import strip_ornaments, strip_whitespace, strip_accidentals
from sjkabc.sjkabc import strip_octave, strip_bar_dividers, expand_notes
from sjkabc.sjkabc import expand_parts, strip_triplets, strip_chords
from sjkabc.sjkabc import strip_extra_chars, expand_abc, HEADER_KEYS
from sjkabc.sjkabc import get_id_from_field, get_field_from_id, strip_decorations
from sjkabc import Tune, Parser


class ABCManipulationTestCase(unittest.TestCase):

    def test_strip_tildes(self):
        abc = "BEE ~B3|Bdf edB|BAF ~F3|DFA BAF|"
        stripped = strip_ornaments(abc)
        self.assertEqual(stripped, 'BEE B3|Bdf edB|BAF F3|DFA BAF|')

    def test_strip_gracenotes(self):
        abc = "ABcd {/d}Bcde|B{/d}B{/A}B e {/dada}eAce|BAGA {dega}BAGA"
        stripped = strip_ornaments(abc)
        self.assertEqual(stripped, 'ABcd Bcde|BBB e eAce|BAGA BAGA')

    def test_strip_trills(self):
        abc = "abcd !trill(!efga|deg!trill)!a bega"
        stripped = strip_ornaments(abc)
        self.assertEqual(stripped, 'abcd efga|dega bega')

    def test_strip_turns(self):
        abc = 'ab!turn!cd baga|baga daga'
        stripped = strip_ornaments(abc)
        self.assertEqual(stripped, 'abcd baga|baga daga')

    def test_strip_fermata(self):
        abc = 'ab!fermata!cd efg!fermata!a|baga baga'
        stripped = strip_ornaments(abc)
        self.assertEqual(stripped, 'abcd efga|baga baga')

    def test_strip_whitespace(self):
        abc = 'abcd efga|dega\r bega\n|{/d}ABcd BEGA'
        stripped = strip_whitespace(abc)
        self.assertEqual(stripped, 'abcdefga|degabega|{/d}ABcdBEGA')

    def test_strip_accidentals(self):
        abc = 'AB^cd e=fga|_abcd =abcd'
        stripped = strip_accidentals(abc)
        self.assertEqual(stripped, 'ABcd efga|abcd abcd')

    def test_strip_octave(self):
        abc = "A,B,CDEFGABcdefgabc'd'e'f'g'a'"
        stripped = strip_octave(abc)
        self.assertEqual(stripped, 'ABCDEFGABcdefgabcdefga')

    def test_strip_bar_dividers(self):
        abc = "abcd abcd|baga BAGA|{/ba}baga DAGA|"
        stripped = strip_bar_dividers(abc)
        self.assertEqual(stripped, "abcd abcdbaga BAGA{/ba}baga DAGA")

    def test_expand_notes(self):
        abc = "G3 EGD|G3 EGD|G2G BGB|d3 BAB"
        expanded = expand_notes(abc)
        self.assertEqual(expanded, 'GGG EGD|GGG EGD|GGG BGB|ddd BAB')

    def test_expand_lone_end_repeat(self):
        abc = "abc abc|bcd bcd|cde cde|def def:|"
        expanded = expand_parts(abc)
        self.assertEqual(expanded, 'abc abc|bcd bcd|cde cde|def def|' +
                         'abc abc|bcd bcd|cde cde|def def|')

    def test_expand_start_and_end_repeat(self):
        abc = '|:abc abc|bcd bcd|cde cde|def def:|'
        expanded = expand_parts(abc)
        self.assertEqual(expanded, 'abc abc|bcd bcd|cde cde|def def|' +
                         'abc abc|bcd bcd|cde cde|def def|')

    def test_expand_two_repeats_first_being_lone(self):
        abc = 'abc abc|bcd bcd|cde cde|def def:|' + \
              '|:bcd bcd|cde cde|def def|efg efg:|'
        expanded = expand_parts(abc)
        self.assertEqual(expanded,
                         'abc abc|bcd bcd|cde cde|def def|' +
                         'abc abc|bcd bcd|cde cde|def def|' +
                         'bcd bcd|cde cde|def def|efg efg|' +
                         'bcd bcd|cde cde|def def|efg efg|')

    def test_expand_two_repeats_(self):
        abc = '|:abc abc|bcd bcd|cde cde|def def:|' + \
              '|:bcd bcd|cde cde|def def|efg efg:|'
        expanded = expand_parts(abc)
        self.assertEqual(expanded,
                         'abc abc|bcd bcd|cde cde|def def|' +
                         'abc abc|bcd bcd|cde cde|def def|' +
                         'bcd bcd|cde cde|def def|efg efg|' +
                         'bcd bcd|cde cde|def def|efg efg|')

    def test_expand_two_repeats_with_double_colon_syntax(self):
        abc = '|:aaa|bbb::' + \
              'ccc|ddd:|'
        expanded = expand_parts(abc)
        self.assertEqual(
            expanded,
            'aaa|bbb|aaa|bbb|ccc|ddd|ccc|ddd|'
        )

    def test_expand_part_with_two_one_bar_endings(self):
        abc = 'abc bcd|abc bcd|1deg bag:|2geg gag||'
        expanded = expand_parts(abc)
        self.assertEqual(expanded,
                         'abc bcd|abc bcd|deg bag|' +
                         'abc bcd|abc bcd|geg gag|')

    def test_expand_part_with_two_one_bar_endings_with_start_repeat(self):
        abc = '|:abc bcd|abc bcd|1deg bag:|2geg gag||'
        expanded = expand_parts(abc)
        self.assertEqual(expanded,
                         'abc bcd|abc bcd|deg bag|' +
                         'abc bcd|abc bcd|geg gag|')

    def test_expand_part_with_two_two_bar_endings(self):
        abc = 'abc bcd|abc bcd|1deg bag|eae eae:|2geg gag|gbg gbg||'
        expanded = expand_parts(abc)
        self.assertEqual(expanded,
                         'abc bcd|abc bcd|deg bag|eae eae|' +
                         'abc bcd|abc bcd|geg gag|gbg gbg|')

    def test_expand_part_with_two_two_bar_endings_with_start_repeat(self):
        abc = '|:abc bcd|abc bcd|1deg bag|eae eae:|2geg gag|gbg gbg||'
        expanded = expand_parts(abc)
        self.assertEqual(expanded,
                         'abc bcd|abc bcd|deg bag|eae eae|' +
                         'abc bcd|abc bcd|geg gag|gbg gbg|')

    def test_expand_two_part_tune_with_two_one_bar_endings(self):
        abc = 'ceec defd|ceaf ecAB|ceec defd|1ceBe cAAB:|2ceBe cAAc||'
        abc += '|:eaae fgaf|e/e/e ef ecAc|eaae fgaf|1ecBe cAAc:|2ecBe cAAB|]'
        expanded = expand_parts(abc)
        self.assertEqual(expanded,
                         'ceec defd|ceaf ecAB|ceec defd|ceBe cAAB|' +
                         'ceec defd|ceaf ecAB|ceec defd|ceBe cAAc|' +
                         'eaae fgaf|e/e/e ef ecAc|eaae fgaf|ecBe cAAc|' +
                         'eaae fgaf|e/e/e ef ecAc|eaae fgaf|ecBe cAAB|')

    def test_expand_three_part_tune(self):
        abc = 'B3B {/d}BAGA|B2GB AGEG|DBB/B/B BAGB|A/B/cBG AGEG|'
        abc += 'B3 B2 A GA|B2GB AGEG|Beed BedB|AdBG A/B/AGE||'
        abc += '|:DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc|1dBAc BGGE:|2dBAc BGBc||'
        abc += '|:d2Bd egge|dB~B2 ABGB|d2Bd egge|1agbg ageg:|2agbg aged|]'
        expanded = expand_parts(abc)
        self.assertEqual(
            expanded,
            'B3B {/d}BAGA|B2GB AGEG|DBB/B/B BAGB|A/B/cBG AGEG|' +
            'B3 B2 A GA|B2GB AGEG|Beed BedB|AdBG A/B/AGE|' +
            'DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc|dBAc BGGE|' +
            'DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc|dBAc BGBc|' +
            'd2Bd egge|dB~B2 ABGB|d2Bd egge|agbg ageg|' +
            'd2Bd egge|dB~B2 ABGB|d2Bd egge|agbg aged|'
        )

    def test_strip_triplets(self):
        abc = "abc (3bbb|bab (3abc|(3GDF bab"
        stripped = strip_triplets(abc)
        self.assertEqual(stripped, 'abc bbb|bab abc|GDF bab')

    def test_strip_chords(self):
        abc = '"Gm" GABd|[C,c]def'
        stripped = strip_chords(abc)
        self.assertEqual(stripped, ' GABd|def')

    def test_strip_extra_chars(self):
        abc = 'A/B/c e<cd>|cBAF ABce\\|dBGA BdcB'
        stripped = strip_extra_chars(abc)
        self.assertEqual(stripped, 'ABc ecd|cBAF ABce|dBGA BdcB')

    def test_expand_abc(self):
        abc = 'A2eA BAec|ABcd egdB|G2dG BGdG|G/G/G dG BAGB|\\'
        abc += 'A2eA BAec|ABcd egdB|GABd eaaf|1gedB BAAG:|2gedB BAce||'
        abc += '|:a2ea ageg|agbg agea|gedc BGBd|~g3a bgeg|\n'
        abc += 'a2ea ageg|agbg ageg|~d3e ~g3e|1dBGB BAce:|2dBGB BAAG|]'
        expected = 'aaeabaecabcdegdbggdgbgdggggdgbagb'
        expected += 'aaeabaecabcdegdbgabdeaafgedbbaag'
        expected += 'aaeabaecabcdegdbggdgbgdggggdgbagb'
        expected += 'aaeabaecabcdegdbgabdeaafgedbbace'

        expected += 'aaeaagegagbgageagedcbgbdgggabgeg'
        expected += 'aaeaagegagbgagegdddegggedbgbbace'
        expected += 'aaeaagegagbgageagedcbgbdgggabgeg'
        expected += 'aaeaagegagbgagegdddegggedbgbbaag'
        processed = expand_abc(abc)
        self.assertEqual(processed, expected)

    def test_tune_object_initialises_empty_lists(self):
        tune = Tune()
        for key in HEADER_KEYS:
            self.assertEqual(getattr(tune, HEADER_KEYS[key]), [])

        for attr in ['abc', 'expanded_abc']:
            self.assertEqual(getattr(tune, attr), [])

    def test_setting_tune_abc_sets_expanded_abc(self):
        t = Tune()
        t.abc = '|:abc bcd|bcd bcd:|'
        self.assertEqual(t.expanded_abc, 'abcbcdbcdbcdabcbcdbcdbcd')

    def test_parser_detects_comment(self):
        p = Parser('blah')
        self.assertTrue(p._line_comment('% This is a test'))

    def test_tune_object_returns_title_string_representation(self):
        t = Tune()
        t.title.append('Test')
        self.assertEqual(str(t), 'Test')

    def test_get_id_from_field_returns_correct_id(self):
        id = get_id_from_field('title')
        self.assertEqual(id, 'T')

    def test_get_field_from_id(self):
        field = get_field_from_id('T')
        self.assertEqual(field, 'title')


class TestDecorations(unittest.TestCase):
    def test_strip_staccatos(self):
        abc = '|:a.b.c.:|'
        self.assertEqual(strip_decorations(abc), '|:abc:|')

    def test_strip_rolls(self):
        abc = '|:a~b~cd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')

    def test_strip_shorthand_fermatas(self):
        abc = '|:aHbcd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')

    def test_strip_shorthand_accent_or_emphasis(self):
        abc = '|:aLbLcd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')

    def test_strip_shorthand_lowermordent(self):
        abc = '|:aMbMcMd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')

    def test_strip_shorthand_codas(self):
        abc = '|:aObOcd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')

    def test_strip_shorthand_uppermordent(self):
        abc = '|:aPbPcPd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')

    def test_strip_shorthand_segno(self):
        abc = '|:aSbScSd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')

    def test_strip_shorthand_trill(self):
        abc = '|:aTbTcTd:|'
        self.assertEqual(strip_decorations(abc), '|:abcd:|')


class TestTune(unittest.TestCase):
    def setUp(self):
        self.t = Tune()
        self.t.book.append('The Bible')
        self.t.composer.append('John Doe')
        self.t.discography.append('Best hits')
        self.t.file.append('http://bogus.url.com/test.abc')
        self.t.group.append('Test')
        self.t.history.append('Interesting')
        self.t.instruction.append('Some instructions')
        self.t.key.append('Gm')
        self.t.note_length.append('1/8')
        self.t.metre.append('4/4')
        self.t.notes.append('A note')
        self.t.origin.append('Sweden')
        self.t.parts.append('AABB')
        self.t.tempo.append('108')
        self.t.rhythm.append('reel')
        self.t.source.append('John Smith')
        self.t.title.append('Test title')
        self.t.title.append('Second test title')
        self.t.index.append('1')
        self.t.transcription.append('Doctor Who')
        self.t.abc.append('|:aaa|bbb|ccc:|')

    def test_get_header_line(self):
        titles = list()
        for title in self.t._get_header_line('title'):
            titles.append(title)

        self.assertEqual(titles, ['T:Test title', 'T:Second test title'])

    def test_format_abc_returns_header_lines_in_correct_order(self):
        correct = """X:1
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
        self.assertEqual(correct, self.t.format_abc())


if __name__ == '__main__':
    unittest.main()
