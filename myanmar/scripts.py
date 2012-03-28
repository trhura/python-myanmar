#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains functions for conversion between unicode and Myanmar legacy
encodings.
To read a database from a file:

>>> dbfile = read(open('test.dat', 'r'))

To split a number:

>>> dbfile.split('01006')
['0', '100', '6']
>>> dbfile.split('902006')
['90', '20', '06']
>>> dbfile.split('909856')
['90', '985', '6']

To split the number and get properties for each part:

>>> dbfile.info('01006')

"""

def convert ():
	print "Hello world!"
