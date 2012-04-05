#!/usr/bin/env python

# setup.py - python-myanmar installation script
#
# Copyright (C) 2012 Thura Hlaing <trhura@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""python-myanmar installation script."""

import os
import sys
from setuptools import setup, find_packages

# fix permissions for sdist
if 'sdist' in sys.argv:
    os.system('chmod -R a+rX .')
    os.umask(int('022', 8))

setup(name='python-myanmar',
      version='0.1',
      packages= find_packages(exclude='tests'),
      package_data={
        'myanmar': ['data/*.json'],
        },
      author='Thura Hlaing',
      author_email='trhura@gmail.com',
      url='http://code.google.com/p/python-myanmar',
      license='GPL-3',
      description='Python Routines for Myanmar Language Processing',
#      long_description=stdnum.__doc__,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing :: General',
          ],
      entry_points = {
        'console_scripts' : ['mmconverter = myanmar._private:convert']
        },
      test_suite = 'tests',
      )
