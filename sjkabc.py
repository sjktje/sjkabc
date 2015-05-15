#!/usr/bin/env python
# encoding: utf-8
"""
Module for parsing text files containing ABC music notation and putting it in
a SQL database.
"""

import json

def abc_header_keys():
    """
    Return a dict of key:name values for supported ABC header keys.

    These are currently:

    A:area
    B:book
    C:composer
    D:discography
    G:group
    H:history
    I:instruction
    K:key
    L:metre
    M:meter
    N:notes
    O:origin
    Q:tempo
    R:rhythm
    S:source
    T:title
    X:index
    Z:transcription
    """

    header_table = """
    A:area
    B:book
    C:composer
    D:discography
    G:group
    H:history
    I:instruction
    K:key
    L:metre
    M:meter
    N:notes
    O:origin
    Q:tempo
    R:rhythm
    S:source
    T:title
    X:index
    Z:transcription
    """

    header_keys = {}

    for line in header_table.split('\n'):
        line = line.strip()

        if line == '':
            continue

        (key, name) = line.split(':')

        header_keys[key] = name

    return header_keys


def parse_file(filename):
    """
    Parse a file containing one or several tunes.

    Return list of dictionaries of lists (jikes).
    """

    header_keys = abc_header_keys()
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
                piece = pieces[-1]
                piece['index'] = line[3:].strip()
                continue

            if in_header:
                (key, value) = line.split(':')
                if key in header_keys:
                    if key == 'K':
                        in_header = False
                    elif header_keys[key] in piece:
                        piece[header_keys[key]].append(value.strip())
                    else:
                        piece[header_keys[key]] = [value.strip()]
            else:
                if 'abc' in piece:
                    piece['abc'].append(line)
                else:
                    piece['abc'] = [line]

    return pieces


if __name__ == "__main__":
    pieces = parse_file('test.abc')
    print json.dumps(pieces, sort_keys=True, indent=4)
