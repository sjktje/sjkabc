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
    """Remove whitespace from string."""
    return abc.replace(' ', '')


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

    repeat_start = 0
    repeat_end = 0
    start = 0
    ret = []

    while True:

        # When there are no more repeats, or if there were none from the
        # beginning, we're done.
        repeat_end = abc.find(':|', start)

        if repeat_end == -1:
            break

        # Starting repeats (|:) are optional (or perhaps even considered
        # ugly?) at the beginning of a tune.
        s = abc.rfind('|:', 0, repeat_end)
        if s != -1:
            repeat_start = s + 2

        # If the repeat end (:|) is followed by a digit, we have more than one
        # ending.
        if len(abc) > repeat_end + 2 and abc[repeat_end + 2].isdigit():
            number_of_bars = 1

            # Go backwards one bar and check if the bar divider is followed by
            # a digit. If not we assume the ending consists of two bars.
            start_of_first_ending = abc.rfind('|', 0, repeat_end)

            if not abc[start_of_first_ending + 1].isdigit():
                start_of_first_ending = abc.rfind('|', 0, start_of_first_ending - 1)
                number_of_bars = 2

            # Doing it this way, we get rid of the digit after the bar
            # divider.
            ret.append(abc[repeat_start:start_of_first_ending])
            ret.append('|')
            ret.append(abc[start_of_first_ending + 2:repeat_end])
            ret.append('|')

            start_of_second_ending = repeat_end + 3
            end_of_second_ending = start_of_second_ending

            # The second ending would probably be the same number of bars as
            # the first.
            while number_of_bars > 0:
                end_of_second_ending = abc.find('|', end_of_second_ending + 1)
                number_of_bars -= 1

            ret.append(abc[repeat_start:start_of_first_ending])
            ret.append('|')
            ret.append(abc[start_of_second_ending:end_of_second_ending])
            ret.append('|')
            start = repeat_end + 2
        else:
            # Repeat (:|) was not followed by a digit, and expansion is easy.
            ret.append(abc[repeat_start:repeat_end])
            ret.append('|')
            ret.append(abc[repeat_start:repeat_end])
            ret.append('|')
            start = repeat_end + 2

    return ''.join(ret)


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
