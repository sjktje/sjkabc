#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup
import sjkabc

setup(
    name='sjkabc',
    version=sjkabc.__version__,
    packages=['sjkabc'],
    author=u'Svante Kvarnström',
    author_email='sjk@sjk.io',
    description='ABC music notation parser',
    url='https://github.com/sjktje/sjkabc',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
    ]
)
