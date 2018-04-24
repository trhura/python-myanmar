# romanizer.py - transliteration module
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

from myanmar.encodings import UnicodeEncoding
from myanmar.language import PhonemicSyllableBreak
from myanmar.language import SIGN_ASAT, SIGN_VIRAMA

__author__ = 'Thura Hlaing'
__email__ = 'trhura@gmail.com'
__version__ = '1.1.0'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018 Thura Hlaing'

from .ipa import IPA  # noqa
from .bgp_pgcn import BGN_PCGN  # noqa


def romanize(string, system, encoding=UnicodeEncoding()):
    """
    Transliterate Burmese text with latin letters.

    >>> romanize("ကွန်ပျူတာ", IPA)
    'kʊ̀ɴpjùtà'
    >>> romanize("ဘင်္ဂလားအော်", BGN_PCGN)
    'bin-gala-aw'
    """

    romans = []

    for syllable in PhonemicSyllableBreak(string, encoding):
        phoneme = syllable['syllable']

        # TODO add more normalization
        if "virama_stack" in syllable:
            phoneme = phoneme.replace(SIGN_VIRAMA, SIGN_ASAT)

        length = len(phoneme)
        string = ""
        scan = 0

        while scan < length:
            # longest matching
            matches = [phoneme[scan:length - i] for i in range(length)]
            for match in matches:
                if match in system.table:
                    string += system.table[match]
                    scan += len(match)
                    break
            else:
                sys.stderr.write("Unable to romanize " + phoneme[scan])
                string += phoneme[scan]
                scan += 1

        if string:  # if not empty
            last = romans[-1] if romans else None  # prev is last here
            roman = system.normalize(string, last)
            romans.append(roman)

    return "".join(romans)
