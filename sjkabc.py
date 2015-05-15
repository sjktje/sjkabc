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


if __name__ == "__main__":
    pieces = parse_file('test.abc')
    # print json.dumps(pieces, sort_keys=True, indent=4)
