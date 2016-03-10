#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sjkabc.sjkabc
    ~~~~~~~~~~~~~

    This module provides functionality for parsing ABC music notation.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.

    .. py:data:: HEADER_KEYS

        Supported ABC notation header keys. This `dict` is used to populate the
        attributes of :py:class:`Tune`.
"""
import os


HEADER_KEYS = dict(
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
    P='parts',
    Q='tempo',
    R='rhythm',
    S='source',
    T='title',
    X='index',
    Z='transcription'
)


class Tune:

    """
    This class represents a parsed tune.

    Its attributes are generated from :py:const:`HEADER_KEYS`, with the
    addition of :py:meth:`abc` and :py:attr:`expanded_abc`.

    Example::

        >>> t = Tune()
        >>> t.title = 'Example tune'
        >>> t.abc = '|:abc abc:|'
        >>> t.expanded_abc
        'abcabcabcabc'

    .. seealso:: :py:const:`HEADER_KEYS`, :py:class:`Parser`
    """

    def __init__(self):
        """Initialise Tune"""
        self._abc = []
        self.expanded_abc = []

        for key in HEADER_KEYS:
            setattr(self, HEADER_KEYS[key], [])

    @property
    def abc(self):
        """Set and get abc property

        Getter/setter for Tune.abc. When set, the attribute `expanded_abc` will
        automatically be set to the expanded ABC.

        :param str abc: abc to set
        :returns: abc

        .. seealso:: :py:func:`expand_abc`

        """
        return self._abc

    @abc.setter
    def abc(self, abc):
        self.expanded_abc = expand_abc(abc)
        return self._abc

    def __str__(self):
        return self.title[0]

    def _get_header_line(self, field):
        """TODO.

        """
        for line in getattr(self, field):
            yield '{}:{}'.format(get_id_from_field(field), line)



class Parser:

    """
    This class provides iterable parsing capabilities.

    `Parser` must be initialised with a string containing ABC music
    notation. This class is iterable and will return a `Tune` object
    for every tune found in the provided ABC notation.

    Example::

        >>> for tune in Parser(abc):
        ...     print('Parsed ', tune.title)

    .. seealso:: :py:class:`Tune`
    """

    def __init__(self, abc):
        """Initialise Parser

        :param abc: string containing ABC to parse

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

        This function will append found ABC tunes to `self.tunes`.

        :param abc: string containing abc to parse

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
                (key, val) = line.split(':', 1)
                if key in HEADER_KEYS:
                    getattr(current_tune, HEADER_KEYS[key]).append(val.strip())

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
        """Check if line is a K: line

        :param str line: line to check
        :returns: True if line is a key line and False if not.
        :rtype: bool

        """
        if line.startswith('K:'):
            return True
        else:
            return False

    def _line_empty(self, line):
        """Check if line is empty

        :param str line: line to check
        :returns: True if line is empty and False if not.
        :rtype: bool

        """
        line = line.strip()
        if line == '':
            return True
        else:
            return False

    def _line_comment(self, line):
        """Check if line is a comment

        :param str line: line to check
        :returns: True if line is a comment and False if not.
        :rtype: bool

        """
        line = line.strip()
        if line.startswith('%'):
            return True
        else:
            return False

    def _line_is_index(self, line):
        """Check if line is an index line (X:).

        If it is, it is considered to be the start of a tune.

        :param str line: line to check
        :returns: True if line is a index line, False if not.
        :rtype: bool

        """
        if line.startswith('X:'):
            return True
        else:
            return False


def get_id_from_field(field):
    """TODO: Docstring

    :param field: TODO
    :returns: TODO

    """
    for key in HEADER_KEYS:
        if HEADER_KEYS[key] == field:
            return key
    else:
        raise KeyError('No such header key: {}'.format(field))


def get_field_from_id(id):
    try:
        return HEADER_KEYS[id]
    except KeyError:
        raise KeyError('No such header key: {}'.format(id))


def parse_file(filename):
    """Run Parser on file contents

    This function is iterable.

    :Example:

        >>> for tune in parse_file('test.abc'):
        ...    print(tune.title)

    :param filename: Name of file to parse
    :returns: :class:`Tune` object for every found tune.
    :rtype: :class:`Tune`

    .. seealso:: :py:func:`parse_dir`, :py:class:`Parser`, :py:class:`Tune`
    """
    with open(filename, 'r') as f:
        abc = f.read()

    for tune in Parser(abc):
        yield tune


def parse_dir(dir):
    """Run :class:`Parser` on every file with .abc extension in `dir`

    :param dir: Directory of abc files
    :returns: :class:`Tune` object for every found file
    :rtype: :class:`Tune`

    .. seealso:: :py:func:`parse_file`, :py:class:`Parser`, :py:class:`Tune`

    """
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in [f for f in filenames if f.endswith('.abc')]:
            for tune in parse_file(os.path.join(dirpath, filename)):
                yield tune


def strip_ornaments(abc):
    """Remove gracenotes, tildes, trills, turns and fermatas from string.

    Example::

        >>> from sjkabc import strip_ornaments
        >>> stripped = strip_ornaments('abc bcd|~c3 def|{/def}efg !trill(!abc|')
        >>> stripped
        'abc bcd|c3 def|efg abc|'

    :param str abc: abc to filter
    :returns: filtered abc
    :rtype: str

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
    """Remove whitespace and newlines from string.

    :param str abc: abc to filter
    :returns: abc with whitespace removed
    :rtype: str
    """
    return ''.join(abc.split())


def strip_accidentals(abc):
    """Remove accidentals from string.

    Example::

        >>> from sjkabc import strip_accidentals
        >>> stripped = strip_whitespace('abc ^c=de|_e^fg _g=fe')
        >>> stripped
        'abc cde|efg gfe'

    :param str abc: abc to filter
    :returns: abc with accidentals removed
    :rtype: str

    """
    for rep in '=^_':
        abc = abc.replace(rep, '')
    return abc


def strip_octave(abc):
    """Remove octave specifiers from string.

    Example::

        >>> from sjkabc import strip_octave
        >>> stripped = strip_octave("A,B,C,d'e'f'")
        >>> stripped
        'ABCdef'

    :param str abc: abc to filter
    :returns: abc with octave specifiers removed
    :rtype: str

    """
    for rep in ',\'':
        abc = abc.replace(rep, '')
    return abc


def strip_bar_dividers(abc):
    """
    Strip bar dividers from string

    This function can safely be run before expand_parts, as it won't remove
    repeats.

    Example::

        >>> from sjkabc import strip_bar_dividers
        >>> stripped = strip_bar_dividers('abcd bcde|bcde abcd|defg abcd|bebe baba')
        >>> stripped
        'abcd bcdebcde abcddefg abcdbebe baba'

    :param str abc: abc to filter
    :returns: abc without bar dividers
    :rtype: str

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

    Example::

        >>> from sjkabc import strip_triplets
        >>> stripped = strip_triplets('AB(3cBA Bcde|fd(3ddd (4efed (4BdBF')
        >>> stripped
        'ABcBA Bcde|fdddd efed BdBF'

    :param str abc: abc to filter
    :returns: abc without triplets
    :rtype: str

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

    :param str abc: abc to expand
    :returns: expanded abc
    :rtype: str
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

    Example::

        >>> print(expand_parts('aaa|bbb|1ccc:|2ddd|]'))
        aaa|bbb|ccc|aaa|bbb|ddd|

    :param str abc: abc to expand
    :returns: expanded abc
    :rtype: str

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

    for rep in ['|:', ':', ']']:
        parsed_abc = parsed_abc.replace(rep, '')
    parsed_abc = parsed_abc.replace('||', '|')

    return parsed_abc


def strip_chords(abc):
    """Strip chords and 'guitar chords' from string.

    Example::

        >>> from sjkabc import strip_chords
        >>> stripped = strip_chords('"G" abc|"Em" bcd|[GBd] cde')
        >>> stripped
        ' abc| bcd | cde'

    :param str abc: abc to filter
    :returns: abc with chords stripped
    :rtype: str

    """
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
    """Strip misc extra chars (/\<>)

    :param str abc: abc to filter
    :returns: filtered abc
    :rtype: str

    """
    for rep in '/\\<>':
        abc = abc.replace(rep, '')
    return abc


def expand_abc(abc):
    """
    Create searchable abc string

    This runs all the stripping and expanding functions on the input string,
    and also makes it lowercase.

    :param str abc: string of abc to expand
    :returns: string of expanded abc
    :rtype: str

    .. seealso:: :py:func:`strip_octave`, :py:func:`strip_accidentals`,
                 :py:func:`strip_triplets`, :py:func:`strip_chords`
                 :py:func:`strip_ornaments`, :py:func:`expand_notes`,
                 :py:func:`expand_parts`, :py:func:`strip_whitespace`
                 :py:func:`strip_bar_dividers`, :py:func:`strip_extra_chars`

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
