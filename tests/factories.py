# -*- coding: utf-8 -*-

import factory
from factory import Iterator, Sequence, lazy_attribute
from sjkabc.sjkabc import Tune


class TuneFactory(factory.Factory):
    class Meta:
        model = Tune

    book = ['The Bible']
    composer = ['Ed Reavy']
    discography = ['Best hits']
    group = ['Group info']
    history = ['Interesting anecdote.']
    instruction = ['Instruction']
    key = ['Gm']
    note_length = ['1/8']
    notes = ['A note']
    origin = ['Sweden']
    title = [
        Sequence(lambda n: 'Tune {}'.format(n)),
        'Test title'
    ]
    parts = ['AABB']
    tempo = ['108']
    rhythm = [Iterator(['reel', 'jig', 'waltz'])]
    source = ['John Smith']
    index = [Sequence(lambda n: '{}'.format(n))]
    transcription = ['Doctor Who']
    abc = ['|:aaa|bbb|ccc:|']

    @lazy_attribute
    def title(self):
        return ['Tune {}'.format(self.index), 'Test title']

    @lazy_attribute
    def file(self):
        return 'http://tunes.sjk.io/tunes/{}/'.format(self.index)

    @lazy_attribute
    def metre(self):
        available_metres = {
            'reel': '4/4',
            'jig': '6/8',
            'waltz': '3/4'
        }
        try:
            return available_metres[self.rhythm[0]]
        except:
            return '4/4'
