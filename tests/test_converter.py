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
            # assert 'အဂၤါ' == converter.convert('အင်္ဂါ', 'unicode', 'zawgyi')
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
