#!/usr/bin/env python
# encoding: utf-8

import json

abc_header_table = """
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

abc_header_keys = {}

for line in abc_header_table.split('\n'):
    line = line.strip()

    if line == '':
        continue

    (key, name) = line.split(':')

    abc_header_keys[key] = name


def parse_file(filename):
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

            if in_header:
                (key, value) = line.split(':')
                if key in abc_header_keys:
                    piece[abc_header_keys[key]] = value.strip()
                    if key == 'K':
                        in_header = False
            else:
                if 'abc' in pieces[-1]:
                    piece['abc'].append(line)
                else:
                    piece['abc'] = [line]

    print json.dumps(pieces, sort_keys=True, indent=4)

if __name__ == "__main__":
    parse_file('test.abc')
