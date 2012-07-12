#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest
import codecs

class TestLanguage (unittest.TestCase):

    def setUp (self):
        self.tests_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path += [os.path.dirname(self.tests_dir)]

        #print sys.path
        try:
            self.l = __import__ ('myanmar.language')
        except Exception, e:
            print e
            sys.exit (-1)

    def test_myfuncs (self):
        import myanmar.language as l

        for i in l.digits_:
            self.assertTrue (l.ismydigit (i))

        for i in l.consonants_:
            self.assertTrue (l.ismyconsonant (i))

        for i in l.medials_:
            self.assertTrue (l.ismymedial (i))

        for i in l.vowels_:
            self.assertTrue (l.ismyvowel (i))

    def test_unicode_repr (self):
        import myanmar.language as l
        fil = codecs.open (os.path.join (self.tests_dir,
                                         'language-tests.txt'),
                                         'r')
        for line in fil.readlines ():
            string = line.strip ()
            #print "----------", string, "----------"
            iter_  = l.ClusterIter (string)
            for i in iter_:
                #print i.encode ('utf-8')
                pass
        fil.close ()


if __name__ == "__main__":
    unittest.main ()
