# -*- coding: utf-8 -*-

import factory
from factory import Iterator, List, post_generation, Sequence
from sjkabc.sjkabc import Tune


class TuneFactory(factory.Factory):
    class Meta:
        model = Tune

    abc = ['|:aaa|bbb|ccc:|']

    @post_generation
    def book(obj, create, extracted, **kwargs):
        obj.book = ['The Bible']

    @post_generation
    def composer(obj, create, extracted, **kwargs):
        obj.composer = ['Ed Reavy']

    @post_generation
    def discography(obj, create, extracted, **kwargs):
        obj.discography = ['Best hits']

    @post_generation
    def group(obj, create, extracted, **kwargs):
        obj.group = ['Group info']

    @post_generation
    def history(obj, create, extracted, **kwargs):
        obj.history = ['Interesting anecdote.']

    @post_generation
    def instruction(obj, create, extracted, **kwargs):
        obj.instruction = ['Instruction']

    @post_generation
    def key(obj, create, extracted, **kwargs):
        obj.key = ['Gm']

    @post_generation
    def note_length(obj, create, extracted, **kwargs):
        obj.note_length = ['1/8']

    @post_generation
    def notes(obj, create, extracted, **kwargs):
        obj.notes = ['A note']

    @post_generation
    def origin(obj, create, extracted, **kwargs):
        obj.origin = ['Sweden']

    @post_generation
    def title(obj, create, extracted, **kwargs):
        obj.title = Sequence(lambda n: ['Test tune {}'.format(n)])
        # obj.title = ['Test tune']

    @post_generation
    def parts(obj, create, extracted, **kwargs):
        obj.parts = ['AABB']


    @post_generation
    def tempo(obj, create, extracted, **kwargs):
        obj.tempo = ['108']

    @post_generation
    def rhythm(obj, create, extracted, **kwargs):
        obj.rhythm = [Iterator(['reel', 'jig', 'waltz'])]

    @post_generation
    def source(obj, create, extracted, **kwargs):
        obj.source = ['John Smith']

    @post_generation
    def index(obj, create, extracted, **kwargs):
        obj.index = [Sequence(lambda n: '{}'.format(n))]

    @post_generation
    def transcription(obj, create, extracted, **kwargs):
        obj.transcription = ['Doctor Who']

    @post_generation
    def file(obj, create, extracted, **kwargs):
        obj.file = [Sequence(lambda n: 'http://tunes.sjk.io/tunes/{}/'.format(n))]

    @post_generation
    def metre(obj, create, extracted, **kwargs):
        obj.metre = ['4/4']
