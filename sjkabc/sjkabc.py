#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sjkabc.sjkabc

This module provides functionality for parsing ABC music notation.

:copyright: (c) 2016 by Svante Kvarnström
:license: BSD, see LICENSE for more details.

.. py:data:: HEADER_KEYS

    Supported ABC notation header keys. This `dict` is used to populate the
    attributes of :class:`Tune`.
"""
import os
import textwrap


HEADER_KEYS = dict(
    B='book',
    C='composer',
    D='discography',
    F='file',
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

#: List of decoration symbols according to the ABC notation standard v2.1.
DECORATIONS = [
    '!trill!', '!trill(!', '!trill)!', '!lowermordent!', '!uppermordent!',
    '!mordent!', '!pralltriller!', '!roll!', '!turn!', '!turnx!',
    '!invertedturn!', '!invertedturnx!', '!arpeggio!', '!>!', '!accent!',
    '!emphasis!', '!fermata!', '!invertedfermata!', '!tenuto!', '!0!', '!1!',
    '!2!', '!3!', '!4!', '!5!', '!+!', '!plus!', '!snap!', '!slide!',
    '!wedge!', '!upbow!', '!downbow!', '!open!', '!thumb!', '!breath!',
    '!pppp!', '!ppp!', '!pp!', '!p!', '!mp!', '!mf!', '!f!', '!ff!', '!fff!',
    '!ffff!', '!sfz!', '!crescendo(!', '!<(!', '!crescendo)!', '!<)!',
    '!diminuendo(!', '!>(!', '!diminuendo)!', '!>)!', '!segno!', '!coda!',
    '!D.S.!', '!D.C.!', '!dacoda!', '!dacapo!', '!fine!', '!shortphrase!',
    '!mediumphrase!', '!longphrase!', '.', '~', 'H', 'L', 'M', 'O', 'P', 'S',
    'T', 'u', 'v'
]


class Tune:

    """
    This class represents a parsed tune.

    Its attributes are generated from :const:`HEADER_KEYS`, with the
    addition of :attr:`abc` and :meth:`expanded_abc`.

    Example::

        >>> t = Tune()
        >>> t.title = 'Example tune'
        >>> t.abc = '|:abc abc:|'
        >>> t.expanded_abc
        'abcabcabcabc'

    .. seealso:: :const:`HEADER_KEYS`, :class:`Parser`
    """

    def __init__(self, **kwargs):
        """Initialise Tune"""
        #: Tune body.
        self.abc = []
        self._expanded_abc = []

        for key in HEADER_KEYS:
            setattr(self, HEADER_KEYS[key], [])

        for keyname, value in kwargs.items():
            try:
                get_id_from_field(keyname)
            except KeyError:
                if keyname not in ['abc']:
                    continue
            setattr(self, keyname, value)

    @property
    def expanded_abc(self):
        """
        Expanded ABC suitable for searching

        :returns: expanded abc
        :rtype: str

        """

        # If possible we should use a cached value.
        if not self._expanded_abc:
            self._expanded_abc = expand_abc(''.join(self.abc))
        return self._expanded_abc

    def __str__(self):
        return self.title[0]

    def _get_header_line(self, field):
        """Retrieve every header/field line

        This function will yield all of the specified `field` lines formatted
        as id:line, for example 'T:Fictional title.' Skips empty lines.

        :param str field: :class:`Tune` attribute containing wanted field

        """
        for line in getattr(self, field):
            if not line:
                continue

            yield wrap_line(line, get_id_from_field(field))

    def format_abc(self):
        """Format ABC tune

        This will return the current :class:`Tune` as a properly formatted
        string, including header fields and ABC.

        :returns: ABC string suitable for writing to file
        :rtype: str

        """
        ret = list()
        for attr in ['index', 'title', 'composer', 'origin', 'rhythm', 'book',
                     'discography', 'file', 'group', 'history', 'notes',
                     'source', 'transcription', 'parts', 'metre',
                     'note_length', 'tempo', 'key']:
            ret += [l for l in self._get_header_line(attr) if len(l) > 2]

        ret += [line for line in self.abc]

        ret.append('\n')

        return '\n'.join(ret)


class Parser:

    """
    This class provides iterable parsing capabilities.

    `Parser` must be initialised with a string containing ABC music
    notation. This class is iterable and will return a `Tune` object
    for every tune found in the provided ABC notation.

    Example::

        >>> for tune in Parser(abc):
        ...     print('Parsed ', tune.title)

    .. seealso:: :class:`Tune`
    """

    def __init__(self, abc=None):
        """Initialise Parser

        :param abc: string containing ABC to parse

        """
        self.tunes = []
        self.last_field = None

        if abc:
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
                    self.last_field = HEADER_KEYS[key]

                # Continuation of info field.
                if key == '+' and self.last_field:
                    field = getattr(current_tune, self.last_field)
                    field[-1] = field[-1] + ' ' + val.strip()

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

    def _line_is_continued_line(self, line):
        """Check if line is a continuation of the last

        :param str line: Line to check
        :returns: true if the line is a continuation line

        """
        if line.startswith('+:'):
            return True
        else:
            return False


def get_id_from_field(field):
    """Get id char from field name

    :param str field: 'long' name of field, for example 'title'
    :returns: id character, for example 'T'
    :rtype: str
    :raises KeyError: if key does not exist.

    """
    for key in HEADER_KEYS:
        if HEADER_KEYS[key] == field:
            return key
    else:
        raise KeyError('No such header key: {}'.format(field))


def get_field_from_id(id):
    """Get long field name from id char.

    :param str id: id char, for example 'T'
    :returns: long field name, like 'title'
    :rtype: str
    :raises KeyError: if key does not exist.

    """
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

    .. seealso:: :func:`parse_dir`, :class:`Parser`, :class:`Tune`
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

    .. seealso:: :func:`parse_file`, :class:`Parser`, :class:`Tune`

    """
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in [f for f in filenames if f.endswith('.abc')]:
            for tune in parse_file(os.path.join(dirpath, filename)):
                yield tune


def strip_ornaments(abc):
    """Remove gracenotes, tildes, trills, turns and fermatas from string.

    Example::

        >>> from sjkabc import strip_ornaments
        >>> stripped = strip_ornaments('abc bcd|~c3 def|{/def}efg !trill(!ab|')
        >>> stripped
        'abc bcd|c3 def|efg ab|'

    :param str abc: abc to filter
    :returns: filtered abc
    :rtype: str

    .. deprecated:: 1.2.0
        Use :func:`strip_gracenotes` and :func:`strip_decorations` instead.

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


def strip_gracenotes(abc):
    """Remove gracenotes

    Example::

        >>> stripped = strip_gracenotes('abc bcd|c3 def|{/def}efg abc|')
        >>> stripped
        'abc bcd|c3 def|efg abc|'

    :param str abc: abc to strip
    :returns: abc stripped from gracenotes
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
        if not in_gracenote:
            tmp.append(c)
    return ''.join(tmp)


def strip_decorations(abc):
    """Remove decorations

    Removes decorations defined in the v2.1 ABC notation standard.

    :param str abc: ABC notation to process
    :returns: stripped ABC
    :rtype: str

    .. seealso:: :const:`DECORATIONS`
    .. versionadded:: 1.2.0

    """
    ret = abc
    for decoration in DECORATIONS:
        ret = ret.replace(decoration, '')

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
        >>> stripped = strip_bar_dividers('abcd bcde|bcde abcd|defg abcd|bebe')
        >>> stripped
        'abcd bcdebcde abcddefg abcdbebe'

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


def strip_slurs(abc):
    """
    Remove slurs from string.

    Example::

        >>> strip_slurs('|:ab(cd) (a(bc)d):|')
        |:abcd abcd:|

    .. warning::
        Don't use this before :func:`strip_decorations` as it may change
        certain decorations so that they wont be recognized. One example would
        be `!trill(!`.

    :param str abc: abc to manipulate
    :returns: abc stripped from slurs
    :rtype: str
    """
    for a in ['(', ')']:
        abc = abc.replace(a, '')
    return abc


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

    parsed_abc = parsed_abc.replace('::', ':||:')

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

    .. seealso:: :func:`strip_octave`, :func:`strip_accidentals`,
                 :func:`strip_triplets`, :func:`strip_chords`
                 :func:`strip_ornaments`, :func:`expand_notes`,
                 :func:`expand_parts`, :func:`strip_whitespace`
                 :func:`strip_bar_dividers`, :func:`strip_extra_chars`,
                 :func:`strip_slurs`

    """
    for f in [strip_octave, strip_accidentals, strip_triplets,
              strip_chords, strip_gracenotes, strip_decorations,
              strip_slurs, expand_notes, expand_parts,
              strip_whitespace, strip_bar_dividers, strip_extra_chars]:
        abc = f(abc)

    return abc.lower()


def wrap_line(string, id, max_length=78, prefix='+'):
    """
    Wrap header line.

    :param str string: string to wrap
    :param str id: character id of header line
    :param int max_length: maximum line length
    :param str prefix: Line prefix for wrapped lines (first line exempted)
    :returns: wrapped line
    :rtype: str

    .. seealso:: :func:`get_id_from_field`
    """
    w = textwrap.TextWrapper()
    w.initial_indent = '{}:'.format(id)
    w.subsequent_indent = '{}:'.format(prefix)
    w.width = max_length
    return '\n'.join(w.wrap(string))
