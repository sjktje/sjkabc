#!/usr/bin/env python
# encoding: utf-8

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
                pieces[-1]['index'] = line[3:]

            if in_header:
                (key, value) = line.split(':')
                if key == 'K':
                    in_header = False
                    pieces[-1]['key'] = value
                elif key == 'T':
                    pieces[-1]['title'] = value
            else:
                if 'abc' in pieces[-1]:
                    pieces[-1]['abc'].append(line)
                else:
                    pieces[-1]['abc'] = [line]

    print pieces

if __name__ == "__main__":
    parse_file('test.abc')
