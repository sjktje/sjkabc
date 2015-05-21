#!/usr/bin/env python
# encoding: utf-8

import unittest
from sjkabc import strip_ornaments, strip_whitespace, strip_accidentals
from sjkabc import strip_octave, strip_bar_dividers, expand_notes
from sjkabc import expand_parts, strip_triplets


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
        self.assertEqual(expanded,
            'B3B {/d}BAGA|B2GB AGEG|DBB/B/B BAGB|A/B/cBG AGEG|' +
            'B3 B2 A GA|B2GB AGEG|Beed BedB|AdBG A/B/AGE|' +
            'DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc|dBAc BGGE|' +
            'DGG/G/G G2BG|G/G/GBG AGEG|DGG/G/G GABc|dBAc BGBc|' +
            'd2Bd egge|dB~B2 ABGB|d2Bd egge|agbg ageg|' +
            'd2Bd egge|dB~B2 ABGB|d2Bd egge|agbg aged|')


    def test_strip_triplets(self):
        abc = "abc (3bbb|bab (3abc|(3GDF bab"
        stripped = strip_triplets(abc)
        self.assertEqual(stripped, 'abc bbb|bab abc|GDF bab')

if __name__ == '__main__':
    unittest.main()
