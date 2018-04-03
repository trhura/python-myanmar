#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import glob
import codecs

from myanmar import converter, encodings


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


def test_zawgyi_syllable_iter():
    for path in glob.glob(
        os.path.join(os.path.dirname(__file__), 'zawgyi-syllable-iter*.txt')
    ):
        with open(path, 'r', encoding='utf-8') as iFile:
            text = iFile.readline().strip()
            syllables = [l.strip('\n') for l in iFile.readlines()]
            print('syllables:', syllables)
            zgy = encodings.ZawgyiEncoding()
            itr = converter.SyllableIter(text=text, encoding=zgy)
            for i, each in enumerate(itr):
                assert each['syllable'] == syllables[i]


def test_unicode_syllable_iter():
    for path in glob.glob(
        os.path.join(os.path.dirname(__file__), 'unicode-syllable-iter*.txt')
    ):
        with open(path, 'r', encoding='utf-8') as iFile:
            text = iFile.readline().strip()
            syllables = [l.strip('\n') for l in iFile.readlines()]

            uni = encodings.UnicodeEncoding()
            itr = converter.SyllableIter(text=text, encoding=uni)

            for i, each in enumerate(itr):
                assert each['syllable'] == syllables[i]


def test_uni2zgy_conversion():
    try:
        path = os.path.join(os.path.dirname(__file__), 'converter-tests.txt')
        fil = codecs.open(path, 'r', encoding='utf-8')
    except Exception as e:
        sys.exit(-1)

    for line in fil.readlines():
        line = line.strip()
        unistr, zgystr = line.split('\t')

        assert zgystr == converter.convert(
            unistr, 'unicode', 'zawgyi'
        )

        fil.close()

def test_zgy2uni_conversion():
    try:
        path = os.path.join(os.path.dirname(__file__), 'converter-tests.txt')
        fil = codecs.open(path, 'r', encoding='utf-8')
    except Exception as e:
        sys.exit(-1)

    for line in fil.readlines():
        line = line.strip()
        unistr, zgystr = line.split('\t')

        assert unistr == converter.convert(
            zgystr, 'zawgyi', 'unicode'
        )

        fil.close()
