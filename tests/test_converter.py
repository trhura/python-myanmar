#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from myanmar import converter


def test_uni2zgy_conversion():
    try:
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'uni2zgy-conversion.txt'
        )
        fil = open(path, 'r', encoding='utf-8')
    except Exception as e:
        sys.exit(-1)

    for line in fil.readlines():
        line = line.strip()
        unistr, zgystr = line.split('\t')

        assert zgystr == converter.convert(unistr, 'unicode', 'zawgyi')
        fil.close()


def test_zgy2uni_conversion():
    try:
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'uni2zgy-conversion.txt'
        )
        fil = open(path, 'r', encoding='utf-8')
    except Exception as e:
        sys.exit(-1)

    for line in fil.readlines():
        line = line.strip()
        unistr, zgystr = line.split('\t')

        assert unistr == converter.convert(zgystr, 'zawgyi', 'unicode')
        fil.close()
