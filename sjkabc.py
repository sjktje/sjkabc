#!/usr/bin/env python
# encoding: utf-8
"""
Module for parsing text files containing ABC music notation and putting it in
a SQL database.
"""
import collections
import json

header_keys = dict(
    A='area',
    B='book',
    C='composer',
    D='discography',
    G='group',
    H='history',
    I='instruction',
    K='key',
    L='metre',
    M='meter',
    N='notes',
    O='origin',
    Q='tempo',
    R='rhythm',
    S='source',
    T='title',
    X='index',
    Z='transcription'
)


def parse_file(filename):
    """
    Parse a file containing one or several tunes.

    Return list of dictionaries of lists (jikes).
    """

    in_header = False
    pieces = []

    with open(filename, 'r') as f:
        for line in f:

            line = line.strip()

            if line == '' or line.startswith('%'):
                continue

            if line[0:2] == 'X:' and line[3].isdigit():
                in_header = True
                pieces.append({})
                pieces[-1] = collections.defaultdict(list)
                piece = pieces[-1]
                piece['index'] = line[3:].strip()
                continue

            if in_header:
                (key, value) = line.split(':')
                if key in header_keys:
                    piece[header_keys[key]].append(value.strip())
                if key == 'K':
                    in_header = False
            else:
                piece['abc'].append(line)

    return pieces


def strip_ornaments(abc):
    """
    Remove gracenotes, tildes, trills, turns and fermatas from string.
    """

    tmp = []
    in_gracenote = False
    for c in abc:
        if c == '{':
            in_gracenote = True
            continue
        if c == '}':
            in_gracenote = False
            continue
        if not in_gracenote and c != '~':
            tmp.append(c)
    ret = ''.join(tmp)
    ret = ret.replace('!trill(!','')
    ret = ret.replace('!trill)!','')
    ret = ret.replace('!turn!','')
    ret = ret.replace('!fermata!','')
    return ret


def strip_whitespace(abc):
    """Remove whitespace and newlines from string."""
    ret = []
    for c in abc:
        if c in [' ', '\n', '\r']:
            continue
        ret.append(c)
    return ''.join(ret)


def strip_accidentals(abc):
    """Remove accidentals from string."""
    ret = []

    for c in abc:
        if c != '=' and c != '^' and c != '_':
            ret.append(c)

    return ''.join(ret)


def strip_octave(abc):
    """Remove octave specifiers from string."""
    ret = []

    for c in abc:
        if c != ',' and c != '\'':
            ret.append(c)

    return ''.join(ret)


def strip_bar_dividers(abc):
    """
    Strip bar dividers from string

    This function can safely be run before expand_parts, as it won't remove
    repeats, e.g.:

    ABCD ABCD|ABCD abcd:|bcde BCDE|]

    becomes

    ABCD ABCDABCD abcd:|bcde BCDE
    """
    ret = []
    prev = None

    for c in abc:
        if (c == '|' and prev != ':') or c == ']':
            continue
        ret.append(c)
        prev = c

    return ''.join(ret)


def strip_triplets(abc):
    """
    Remove duplets, triplets, quadruplets, etc from string.

    Please note that this simply removes the (n and leaves the following
    notes.
    """
    ret = []
    abc_len = len(abc)
    i = 0

    while i < abc_len:
        if abc[i] == '(' and abc_len > i+1 and abc[i+1].isdigit():
            i += 2
        else:
            ret.append(abc[i])
            i += 1

    return ''.join(ret)


def expand_notes(abc):
    """
    Expand notes, so that E2 becomes EE et.c.
    """

    ret = []
    prev = None
    for c in abc:
        if c.isdigit() and (prev.isalpha() or prev in [',' '\'']):
            ret.append(prev * (int(c)-1))
        else:
            ret.append(c)

        prev = c

    return ''.join(ret)


def expand_parts(abc):
    """
    Expand repeats with support for (two) alternate endings.

    In other words:

        |:aaa|bbb|1ccc|ddd:|2eee|fff||

    becomes:

        aaa|bbb|ccc|ddd|aaa|bbb|eee|fff

    An alternate ending may contain a maximum of two bars, as per ABC
    standard. There may be a maximum of two alternative endings. Although one
    could do more than two endings in ABC, using P:parts, I hardly ever see it
    and therefore have not implemented support for it here. In Henrik
    Norbeck's tune collection (May 2015), there was not a single one of the
    2312 tunes that contained a third ending. Enough said.
    """
    parsed_abc = abc
    start = 0
    end = 0

    while True:
        end = parsed_abc.find(':|', start)
        if (end == -1):
            break

        new_start = parsed_abc.rfind('|:', 0, end)
        if (new_start != -1):
            start = new_start+2

        tmp = []
        if end + 2 < len(parsed_abc) and parsed_abc[end+2].isdigit():
            first_ending_start = parsed_abc.rfind('|', 0, end)
            num_bars = 1
            if not parsed_abc[first_ending_start+1].isdigit():
                first_ending_start = parsed_abc.rfind('|', 0, first_ending_start)
                num_bars = 2

            tmp.append(parsed_abc[start:first_ending_start])
            tmp.append('|')
            tmp.append(parsed_abc[first_ending_start+2:end])
            tmp.append('|')

            second_ending_start = end+2
            second_ending_end = None
            for i in xrange(num_bars):
                second_ending_end = parsed_abc.find('|', second_ending_start)

            tmp.append(parsed_abc[start:first_ending_start])
            tmp.append('|')
            tmp.append(parsed_abc[second_ending_start+1:second_ending_end])
            parsed_abc = parsed_abc.replace(
                                    parsed_abc[start:second_ending_end],
                                    ''.join(tmp), 1)
            start += len(tmp)
        else:
            tmp.append(parsed_abc[start:end])
            tmp.append('|')
            tmp.append(parsed_abc[start:end])
            tmp.append('|')
            parsed_abc = parsed_abc.replace(parsed_abc[start:end+2],
                                          ''.join(tmp), 1)
            start += len(tmp)

    parsed_abc = parsed_abc.replace('|:', '').replace(':', '').replace('||', '|').replace(']', '')
    return parsed_abc


def strip_chords(abc):
    """Strip chords and 'guitar chords' from string."""
    ret = []
    in_chord = False

    for c in abc:
        if c == '[' or (c == '"' and not in_chord):
            in_chord = True
        elif c == ']' or (c == '"' and in_chord):
            in_chord = False
        elif in_chord:
            continue
        else:
            ret.append(c)

    return ''.join(ret)


def strip_extra_chars(abc):
    ret = []
    for c in abc:
        if c in ['/', '\\', '<', '>']:
            continue
        ret.append(c)
    return ''.join(ret)


def expand_abc(abc):
    """
    Create searchable abc string

    This runs all the stripping and expanding functions on the input string,
    and also makes it lowercase.
    """
    ret = strip_octave(abc)
    ret = strip_accidentals(ret)
    ret = strip_triplets(ret)
    ret = strip_chords(ret)
    ret = strip_ornaments(ret)
    ret = expand_notes(ret)
    ret = expand_parts(ret)
    ret = strip_whitespace(ret)
    ret = strip_bar_dividers(ret)
    ret = strip_extra_chars(ret)
    ret = ret.lower()
    return ret


if __name__ == "__main__":
    pieces = parse_file('test.abc')
    # print json.dumps(pieces, sort_keys=True, indent=4)
    # expand_parts("abc abc|bcd bcd|bab bab|]")
    abc = "|:a b|c d:|\n|:A B|C D:|"
    abc += "|:e f|g A|1B C:|2D E||"
    # abc = "aaa|bbb|ccc:|"
    # abc = "|:aaa|bbb|1ccc:|2ddd|"
    print abc
    print expand_parts(abc)


