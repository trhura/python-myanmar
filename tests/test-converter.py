#! /usr/bin/env python
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

class TestConversion (unittest.TestCase):

    def setUp (self):
        pass

    def test_conversion (self):
        try:
            path = os.path.join (os.path.dirname(__file__), 'converter-tests.txt')
            fil = codecs.open (path, 'r', encoding='utf-8')
        except Exception, e:
            print e
            sys.exit (-1)

        for line in fil.readlines ():
            line = line.strip ()
            strs = line.split ('\t')
            encodings = converter.get_available_encodings ()
            encodings.sort ()
            if len(strs) != len(encodings):
                continue

            i = 0
            strings = {}
            for encoding in encodings:
                strings[encoding] = strs[i]
                i += 1

            for encoding in encodings:
                if strings[encoding] == '-':
                    continue
                self.assertEqual (strings[encoding],
                                  converter.convert (strings['unicode'], 'unicode', encoding))
                self.assertEqual (strings['unicode'],
                                  converter.convert (strings[encoding], encoding, 'unicode'))

if __name__ == "__main__":
    unittest.main ()
