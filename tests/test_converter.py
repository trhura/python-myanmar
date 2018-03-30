#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import unittest
import sys
import os
import codecs
# import imp

# tests_dir = os.path.dirname(os.path.abspath(__file__))
# root_dir = os.path.dirname(tests_dir)

# sys.path += [os.path.join(root_dir, 'myanmar')]
# converter = imp.load_source(
#     'converter', os.path.join(root_dir, 'myanmar', 'converter.py')
# )

from myanmar import converter


def test_conversion():
    try:
        path = os.path.join(os.path.dirname(__file__), 'converter-tests.txt')
        fil = codecs.open(path, 'r', encoding='utf-8')
    except Exception as e:
        sys.exit(-1)

    for line in fil.readlines():
        line = line.strip()
        strs = line.split('\t')
        encodings = converter.get_available_encodings()
        encodings.sort()
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
            assert strings[encoding] == converter.convert(
                strings['unicode'], 'unicode', encoding
            )
            assert strings['unicode'] == converter.convert(
                strings[encoding], encoding, 'unicode'
            )
            assert strings[encoding] == converter.convert(
                strings['wininnwa'], 'wininnwa', encoding
            )
            assert strings['wininnwa'] == converter.convert(
                strings[encoding], encoding, 'wininnwa'
            )
            assert strings[encoding] == converter.convert(
                strings['zawgyi'], 'zawgyi', encoding
            )
            assert strings['zawgyi'] == converter.convert(
                strings[encoding], encoding, 'zawgyi'
            )
        fil.close()