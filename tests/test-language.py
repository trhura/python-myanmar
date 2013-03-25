#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import codecs

tests_dir   = os.path.dirname(os.path.abspath(__file__))
root_dir    = os.path.dirname(tests_dir)

import imp
sys.path += [os.path.join (root_dir, 'myanmar')]
ml = imp.load_source ('language',
                      os.path.join (root_dir,
                                    'myanmar',
                                    'language.py'))

class TestLanguage (unittest.TestCase):

    def setUp (self):
        pass

    def test_myfuncs (self):
        for i in ml.digits:
            self.assertTrue (ml.ismydigit (i))

        for i in ml.consonants:
            self.assertTrue (ml.ismyconsonant (i))

        for i in ml.medials:
            self.assertTrue (ml.ismymedial (i))

        for i in ml.vowels:
            self.assertTrue (ml.ismyvowel (i))

    def test_unicode_repr (self):
        fil = codecs.open (os.path.join (tests_dir,
                                         'language-tests.txt'),
                                         'r')
        for line in fil.readlines ():
            string = line.strip ()
            print "----------", string, "----------"
            iter_  = ml.ClusterIter (string)
            for i in iter_:
                print i.encode ('utf-8')
                pass
        fil.close ()


if __name__ == "__main__":
    unittest.main ()
