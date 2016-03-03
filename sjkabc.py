#!/usr/bin/env python
# encoding: utf-8
"""
Module for parsing ABC music notation.
"""
import os

HEADER_KEYS = dict(
    A='area',
    B='book',
    C='composer',
    D='discography',
    G='group',
    H='history',
    I='instruction',
    K='key',
    L='note_length',
    M='metre',
    N='notes',
    O='origin',
    Q='tempo',
    R='rhythm',
    S='source',
    T='title',
    X='index',
    Z='transcription'
)


class Tune:

    """TODO: Tune class docstring"""

    def __init__(self):
        """Initialise Tune"""
        self.abc = []
        self.expanded_abc = []

        for key in HEADER_KEYS:
            setattr(self, HEADER_KEYS[key], [])

    def __str__(self):
        return self.title[0]

class Parser:

    def __init__(self, abc):
        """TODO: Docstring for __init__.
        :param: src string
        :returns: TODO

        """
        self.tunes = []
        self.parse(abc)
        self.index = len(self.tunes)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.tunes[self.index]

    def parse(self, abc):
        """Parse ABC notation.

        :param abc: string containing abc to parse
        :returns: `Tune`

        """
        in_header = False
        current_tune = None

        for line in abc.splitlines():
            if self._line_empty(line) or self._line_comment(line):
                continue

            # At beginning of header
            if self._line_is_index(line):
                if current_tune:
                    # We have a parsed tune already, append it to list of
                    # tunes.
                    self.tunes.append(current_tune)

                in_header = True
                current_tune = Tune()

            if in_header:
                (key, value) = line.split(':', 1)
                if key in HEADER_KEYS:
                    getattr(current_tune, HEADER_KEYS[key]).append(value.strip())

                # Header ends at K:
                if self._line_is_key(line):
                    in_header = False

            else:
                if current_tune:
                    current_tune.abc.append(line)

        else:
            if current_tune:
                self.tunes.append(current_tune)

    def _line_is_key(self, line):
        """TODO: Docstring for _line_is_key.

        :param line: TODO
        :returns: TODO

        """
        if line.startswith('K:'):
            return True
        else:
            return False

    def _line_empty(self, line):
        line = line.strip()
        if line == '':
            return True
        else:
            return False

    def _line_comment(self, line):
        line = line.strip()
        if line.startswith('%'):
            return True
        else:
            return False

    def _line_is_index(self, line):
        """Check if line is an index line (X:).

        :param line: TODO
        :returns: TODO

        """
        if line.startswith('X:'):
            return True
        else:
            return False


def parse_file(filename):
    """
    Like parse_abc but operates on a file.
    """
    with open(filename, 'r') as f:
        abc = f.read()

    for tune in Parser(abc):
        yield tune


def parse_dir(dir):
    """
    Same as parse_file, but works recursively on all .abc files in dir.
    """
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in [f for f in filenames if f.endswith('.abc')]:
            for tune in parse_file(os.path.join(dirpath, filename)):
                yield tune


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
    for rep in ['!trill(!', '!trill)!', '!turn!', '!fermata!']:
        ret = ret.replace(rep, '')
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
                first_ending_start = parsed_abc.rfind('|', 0,
                                                      first_ending_start)
                num_bars = 2

            tmp.append(parsed_abc[start:first_ending_start])
            tmp.append('|')
            tmp.append(parsed_abc[first_ending_start+2:end])
            tmp.append('|')

            second_ending_start = end+2
            second_ending_end = None
            for i in range(num_bars):
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

    parsed_abc = parsed_abc.replace('|:', '')
    parsed_abc = parsed_abc.replace(':', '')
    parsed_abc = parsed_abc.replace('||', '|')
    parsed_abc = parsed_abc.replace(']', '')
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
    for tune in parse_file('test.abc'):
        print(tune)
