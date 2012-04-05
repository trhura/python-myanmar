#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import codecs

class TestConversion (unittest.TestCase):

    def setUp (self):
        sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
        print sys.path
        try:
            import myanmar.converter
        except Exception, e:
            print e
            sys.exit (-1)

    def test_conversion (self):
        import myanmar.converter as converter
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
                self.assertEqual (strings[encoding],
                                  converter.convert (strings['unicode'], 'unicode', encoding))
                self.assertEqual (strings['unicode'],
                                  converter.convert (strings[encoding], encoding, 'unicode'))

if __name__ == "__main__":
    unittest.main ()
