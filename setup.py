#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup
import sjkabc

setup(name='sjkabc',
      version=sjkabc.__version__,
      description='ABC music notation parser',
      author='Svante Kvarnström',
      author_email='sjk@sjk.io',
      url='https://github.com/sjktje/sjkabc',
      py_modules=['sjkabc'],
)
