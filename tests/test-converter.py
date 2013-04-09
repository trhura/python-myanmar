#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import glob
import json

tests_dir   = os.path.dirname(os.path.abspath(__file__))
root_dir    = os.path.dirname(tests_dir)

import imp
sys.path += [os.path.join (root_dir, 'myanmar')]
converter = imp.load_source ('converter',
                             os.path.join (root_dir,
                                           'myanmar',
                                           'converter.py'))
encodings = imp.load_source ('encodings',
                             os.path.join (root_dir,
                                           'myanmar',
                                           'encodings.py'))

class TestConversion (unittest.TestCase):

    def setUp (self):
        self.maxDiff = None

    def test_json_files (self):
        uni = encodings.UnicodeEncoding ()
        zgy = encodings.ZawgyiEncoding ()

        def sub_keys (json):
            ret = []
            for key, value in json.items ():
                ret += json[key].keys ()
            return ret

        self.assertEqual (sorted(uni.json_data.keys ()),
                          sorted(zgy.json_data.keys ()))

        self.assertEqual (sorted(sub_keys(uni.json_data)),
                          sorted(sub_keys(zgy.json_data)))

    def test_zawgyi_syllable_iter (self):
        for path in glob.glob (os.path.join (os.path.dirname (__file__),
                                            'zawgyi-syllable-iter*.txt')):
            with open (path, 'r', encoding='utf-8') as iFile:
                text = iFile.readline().strip ()
                syllables = [l.strip('\n') for l in iFile.readlines()]

                zgy = encodings.ZawgyiEncoding ()
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

                uni = encodings.UnicodeEncoding ()
                itr = converter.SyllableIter (text=text, encoding=uni)

                for i, each in enumerate(itr):
                    #print (each)
                    self.assertEqual (each['syllable'], syllables[i])

if __name__ == "__main__":
    unittest.main ()
