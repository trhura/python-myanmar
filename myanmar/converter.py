# converter.py - converter module
# coding: utf-8
# The MIT License (MIT)
# Copyright (c) 2018 Thura Hlaing

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import sys

from myanmar import language
from myanmar import encodings


def get_supported_encodings():
    """
    Get a list of encodings supported by ``converter`` module.

    >>> get_supported_encodings()
    ['unicode', 'zawgyi', 'wininnwa']
    """
    return ['unicode', 'zawgyi', 'wininnwa']


encoders = {
    "unicode": encodings.UnicodeEncoding(),
    "zawgyi": encodings.ZawgyiEncoding(),
    "wininnwa": encodings.WininnwaEncoding(),
}


def convert(text, fromenc, toenc):
    """
    Convert text in ``fromenc`` encoding to ``toenc`` encoding.

    >>> convert('အကျိုးတရား', 'unicode', 'zawgyi')
    'အက်ိဳးတရား'
    >>> convert('ဉာဏ္ႀကီးရွင္', 'zawgyi', 'unicode')
    'ဉာဏ်ကြီးရှင်'
    >>> convert('&[ef;', 'wininnwa', 'unicode')
    'ရဟန်း'
    """
    if fromenc not in encoders:
        raise NotImplementedError("Unsupported encoding: %s" % fromenc)

    if toenc not in encoders:
        raise NotImplementedError("Unsupported encoding: %s" % toenc)

    fromencoder = encoders[fromenc]
    toencoder = encoders[toenc]
    iterator = language.MorphoSyllableBreak(text=text, encoding=fromencoder)

    otext = ""
    for syllable in iterator:
        full_syllable = syllable['syllable']
        if len(syllable) == 1:
            # unmatched text, no need to convert
            otext += full_syllable
            continue

        if full_syllable in fromencoder.reverse_table:
            # Direct mapping
            key = fromencoder.reverse_table[full_syllable]
            key = key[:key.find('_')] if '_' in key else key  # remove _part
            otext += toencoder.table[key]
            continue

        otext += convert_syllable(syllable, fromenc, toenc)

    return otext


def convert_syllable(syllable, fromenc, toenc):
    fromencoder = encoders[fromenc]
    toencoder = encoders[toenc]

    for part in syllable.keys():
        if part == 'syllable': continue  # noqa skip complete syllable

        key = fromencoder.reverse_table[syllable[part]]
        key = key[:key.find('_')] if '_' in key else key  # remove _part

        if part == "consonant":
            if key == "na":
                key += choose_na_variant(syllable)
            if key == "ra":
                key += choose_ra_variant(syllable)
            if key == "nnya":
                key += choose_nnya_variant(syllable)
        elif part == "yapin":
            key += choose_yapin_variant(syllable)
        elif part == "yayit":
            key += choose_yayit_variant(syllable)
        elif part == "uVowel":
            key += choose_uvowel_variant(syllable)
        elif part == "aaVowel":
            key += choose_aavowel_variant(syllable)
        elif part == "dotBelow":
            key += choose_dot_below_variant(syllable)

        syllable[part] = key

    if 'uVowel' in syllable and 'hatoh' in syllable:
        syllable['hatoh'] = syllable['hatoh'] + '-' + syllable['uVowel']
        del syllable['uVowel']
    if 'wasway' in syllable and 'hatoh' in syllable:
        syllable['wasway'] = syllable['wasway'] + '-' + syllable['hatoh']
        del syllable['hatoh']

    osyllable = ""
    # collect codepoints in syllable, in correct syllable order
    for part in toencoder.syllable_parts:
        if part not in syllable: continue  # noqa

        try:
            key = syllable[part]
            osyllable += toencoder.table[key]
        except Exception:
            print(key, syllable)

    return osyllable


def is_wide_consonant(char):
    WIDE_CONSONANTS = [
        "ka", "gha", "ca", "cha", "nya", "nna", "ta", "tha", "bha", "ya", "la",
        "sa", "ha", "a", "greatSa"
    ]
    return char in WIDE_CONSONANTS


def is_lower_consonant(char):
    LOWER_CONSONANTS = [
        "nya",
        "na",
        "ra",  # ... more
    ]
    return char in LOWER_CONSONANTS


def has_lower_marks(syllable, filters=[]):
    MAKRS = ["stack", "wasway", "yapin", "yayit", "hatoh", "uVowel"]
    for mark in [m for m in MAKRS if m not in filters]:
        if mark in syllable:
            return True
    return False


def has_upper_marks(syllable, filters=[]):
    MAKRS = ["kinzi", "yapin", "iVowel", "aiVowel", "anusvara"]
    for mark in [m for m in MAKRS if m not in filters]:
        if mark in syllable:
            return True
    return False


def choose_ra_variant(syllable):
    key = "_alt" if has_lower_marks(syllable, ["hatoh"]) else ""
    return key


def choose_na_variant(syllable):
    key = "_alt" if has_lower_marks(syllable) else ""
    return key


def choose_nnya_variant(syllable):
    key = "_alt" if has_lower_marks(syllable) else ""
    return key


def choose_uvowel_variant(syllable):
    key = "_tall" if has_lower_marks(syllable, ["uVowel", "hatoh"]) else ""
    return key


def choose_aavowel_variant(syllable):
    _C = ["kha", "gha", "nga", "da", "dha", "pa", "wa"]

    key = ""
    if syllable['consonant'] in _C:
        for c in ['yapin', 'yayit', 'wasway', 'hatoh']:
            if c in syllable:
                break
        else:
            key += '_tall'

    return key


def choose_yayit_variant(syllable):
    key = "_wide" if is_wide_consonant(syllable['consonant']) else "_narrow"
    key += "_lower" if has_lower_marks(syllable, ["yayit", "uVowel"]) else ""
    key += "_upper" if has_upper_marks(syllable, ["yayit"]) else ""
    return key


def choose_yapin_variant(syllable):
    key = "_alt" if has_lower_marks(syllable, ["yapin", "uVowel"]) else ""
    return key


def choose_dot_below_variant(syllable):
    key = ""

    if syllable['consonant'] == "na":
        key += "_alt"
    elif syllable['consonant'] == "ra":
        key += "_alt_alt"
    elif "uVowel" in syllable:
        key += "_alt_alt" if 'yayit' in syllable else '_alt'
    elif "yapin" in syllable:
        key += "_alt"
    elif "wasway" in syllable:
        key += "_alt_alt"

    return key


def main():
    import argparse
    import fileinput

    parser = argparse.ArgumentParser(
        description='Convert between various Myanmar encodings'
    )
    parser.add_argument(
        '-f',
        '--from',
        dest='fro',
        action='store',
        required=True,
        help='convert characters from ENCODING',
        metavar="ENCODING",
    )
    parser.add_argument(
        '-t',
        '--to',
        dest='to',
        action='store',
        required=True,
        help='convert characters to ENCODING',
        metavar="ENCODING",
    )
    parser.add_argument(
        'files',
        metavar='FILE',
        nargs='*',
        help='files to convert, if empty, stdin is used'
    )

    args = parser.parse_args()
    if args.fro not in get_supported_encodings():
        print(
            "%s is not a supported encoding. Should be any of %s." %
            (args.fro, get_supported_encodings())
        )
        sys.exit(-1)

    if args.to not in get_supported_encodings():
        print(
            "%s is not a supported encoding. Should be any of %s." %
            (args.to, get_supported_encodings())
        )
        sys.exit(-1)

    if args.fro == args.to:
        print("from encoding must not be the same as to encoding.")
        sys.exit(-1)

    for line in fileinput.input(files=args.files):
        print(convert(line, args.fro, args.to), end='')


if __name__ == "__main__":
    main()
