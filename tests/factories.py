# -*- coding: utf-8 -*-

import factory
from factory import Iterator, Sequence
from sjkabc.sjkabc import Tune


class TuneFactory(factory.Factory):
    class Meta:
        model = Tune

    abc = ['|:aaa|bbb|ccc:|']
    book = ['The Bible']
    composer = ['Ed Reavy']
    discography = ['Greatest hits']
    file = Sequence(lambda n: ['http://tunes.sjk.io/tunes/{}'.format(n)])
    group = ['Group info']
    history = ['Interesting anecdote.']
    index = Sequence(lambda n: ['1'.format(n)])
    instruction = ['Instruction']
    key = Iterator(['Gm', 'Am', 'D'])
    metre = ['4/4']
    note_length = ['1/8']
    notes = ['A note']
    origin = ['Sweden']
    parts = ['AABB']
    rhythm = ['reel']
    source = ['John Smith']
    tempo = ['108']
    title = ['Test tune']
    transcription = ['Doctor Who']
