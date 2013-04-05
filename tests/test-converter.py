#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import codecs

tests_dir   = os.path.dirname(os.path.abspath(__file__))
root_dir    = os.path.dirname(tests_dir)

import imp
sys.path += [os.path.join (root_dir, 'myanmar')]
converter = imp.load_source ('converter',
                             os.path.join (root_dir,
                                           'myanmar',
                                           'converter.py'))

import glob

class TestConversion (unittest.TestCase):

    def setUp (self):
        pass

    def test_zawgyi_syllable_iter (self):
        for path in glob.glob (os.path.join (os.path.dirname (__file__),
                                            'zawgyi-syllable-iter*.txt')):
            with open (path, 'r', encoding='utf-8') as iFile:
                text = iFile.readline().strip ()
                syllables = [l.strip('\n') for l in iFile.readlines()]

                zgy = converter.ZawgyiEncoding ('zawgyi.json')
                itr = converter.SyllableIter (text=text, encoding=zgy)

                for i, each in enumerate(itr):
                    #print (each)
                    self.assertEqual (each['syllable'], syllables[i])

    def test_unicode_syllable_iter (self):
        for path in glob.glob (os.path.join (os.path.dirname (__file__),
                                            'unicode-syllable-iter*.txt')):
            with open (path, 'r', encoding='utf-8') as iFile:
                text = iFile.readline().strip ()
                syllables = [l.strip('\n') for l in iFile.readlines()]

                uni = converter.UnicodeEncoding ('unicode.json')
                itr = converter.SyllableIter (text=text, encoding=uni)

                for i, each in enumerate(itr):
                    #print (each)
                    self.assertEqual (each['syllable'], syllables[i])

if __name__ == "__main__":
    unittest.main ()
