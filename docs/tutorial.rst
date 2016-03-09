Tutorial
========

:mod:`sjkabc` provides a set of functions that parses `ABC music notation`_. There are currently three major types of functions:

* strip functions:
  These all begin with `strip_`. The strip functions return the passed string stripped from, for example, ornaments or accidentals. These functions can be used to create simplified notation suitable for searching.

* expand functions:
  These functions will expand repeats, multiple endings, and 'long notes'. These functions are also valuable for creating searchable ABC.

* parse functions:
  These are helper functions which use :class:`~sjkabc.Parser` to parse files and directories.

The two core classes in :mod:`sjkabc` are :class:`~sjkabc.Parser` and :class:`~sjkabc.Tune`, which are used to parse and
describe pieces of ABC music.

.. _`ABC music notation`: http://abcnotation.com/wiki/abc:standard:v2.1

Basic usage
-----------

Parsing a string of ABC
^^^^^^^^^^^^^^^^^^^^^^^

The :class:`~sjkabc.Parser` class is iterable, and will return :class:`~sjkabc.Tune` objects representing ABC tunes found in the input string. Here's an example of how to parse a tune and print its title:

.. code-block:: python

    from sjkabc import Parser

    abc_string = """
    X: 37
    T: Apples In Winter
    C: Trad.
    R: Jig
    M: 6/8
    L: 1/8
    K: Em
    BEE BEE|Bdf edB|BAF FEF|DFA BAF|
    BEE BEE|Bdf edB|BAB dAF|1FED EGA:|2FED EAc||
    |:e2f gfe|eae edB|BAF FEF|DFA BAF|
    e2f gfe|eae edB|BAB dAF|1FED EAc:|2FED E3|]
    """
    for tune in Parser(abc_string):
        print tune.title[0]

Not all ABC header keys may be defined several times, but all Parser attributes
are lists for the sake of consistency. Several titles may, for example, be
defined simply by using several T: statements, but only one index number (X:)
is permitted.

Parsing a file
^^^^^^^^^^^^^^

The :func:`~sjkabc.parse_file` helper function is used to parse files containing ABC
notation. For example:

.. code-block:: python

    from sjkabc import parse_file

    for tune in parse_file('test.abc'):
        print('Parsed {} with index number {}.'.format(tune.title[0], tune.index[0])


Parsing a directory of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To parse all .abc files in a directory, one may use :func:`~sjkabc.parse_dir`, which
works in the same fashion as :func:`~sjkabc.parse_file`.

.. code-block:: python

    from sjkabc import parse_dir

    for tune in parse_dir('/data/music/abc/'):
        print('Parsed {} with index number {}.'.format(tune.title[0], tune.index[0])
