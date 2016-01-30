#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import twitter_utils

setup(name='twitter_utils',
      version=twitter_utils.version,
      description='Series of utility functions for twitter',
      url='http://github.com/geosoco/twitter_utils',
      author='John Robinson',
      author_email='pubsoco@geosoco.com',
      license='BSD',
      packages=['twitter_utils'],
      platforms='any',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
      ])