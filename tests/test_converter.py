#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from myanmar import converter
from myanmar import encodings


def test_json_files():
    uni = encodings.UnicodeEncoding()
    zgy = encodings.ZawgyiEncoding()

    def sub_keys(json):
        ret = []
        for key, value in json.items():
            ret += json[key].keys()
        return ret

    assert sorted(uni.json_data.keys()) == sorted(zgy.json_data.keys())
    assert sorted(sub_keys(uni.json_data)) == sorted(sub_keys(zgy.json_data))


def test_uni2zgy_conversion():
    try:
        path = os.path.join(os.path.dirname(__file__), 'converter-tests.txt')
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
        path = os.path.join(os.path.dirname(__file__), 'converter-tests.txt')
        fil = open(path, 'r', encoding='utf-8')
    except Exception as e:
        sys.exit(-1)

    for line in fil.readlines():
        line = line.strip()
        unistr, zgystr = line.split('\t')

        assert unistr == converter.convert(zgystr, 'zawgyi', 'unicode')
        fil.close()
