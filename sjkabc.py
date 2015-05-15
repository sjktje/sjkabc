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


if __name__ == "__main__":
    pieces = parse_file('test.abc')
    print json.dumps(pieces, sort_keys=True, indent=4)
