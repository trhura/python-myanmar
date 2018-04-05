# language.py - language module
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

from myanmar import encodings

LETTER_KA = chr(0x1000)
LETTER_KHA = chr(0x1001)
LETTER_GA = chr(0x1002)
LETTER_GHA = chr(0x1003)
LETTER_NGA = chr(0x1004)
LETTER_CA = chr(0x1005)
LETTER_CHA = chr(0x1006)
LETTER_JA = chr(0x1007)
LETTER_JHA = chr(0x1008)
LETTER_NYA = chr(0x1009)
LETTER_NNYA = chr(0x100a)
LETTER_TTA = chr(0x100b)
LETTER_TTHA = chr(0x100c)
LETTER_DDA = chr(0x100d)
LETTER_DDHA = chr(0x100e)
LETTER_NNA = chr(0x100f)
LETTER_TA = chr(0x1010)
LETTER_THA = chr(0x1011)
LETTER_DA = chr(0x1012)
LETTER_DHA = chr(0x1013)
LETTER_NA = chr(0x1014)
LETTER_PA = chr(0x1015)
LETTER_PHA = chr(0x1016)
LETTER_BA = chr(0x1017)
LETTER_BHA = chr(0x1018)
LETTER_MA = chr(0x1019)
LETTER_YA = chr(0x101a)
LETTER_RA = chr(0x101b)
LETTER_LA = chr(0x101c)
LETTER_WA = chr(0x101d)
LETTER_SA = chr(0x101e)
LETTER_HA = chr(0x101f)
LETTER_LLA = chr(0x1020)
LETTER_A = chr(0x1021)
LETTER_SHAN_A = chr(0x1022)
LETTER_I = chr(0x1023)
LETTER_II = chr(0x1024)
LETTER_U = chr(0x1025)
LETTER_UU = chr(0x1026)
LETTER_E = chr(0x1027)
LETTER_MON_E = chr(0x1028)
LETTER_O = chr(0x1029)
LETTER_AU = chr(0x102a)
VOWEL_SIGN_TALL_AA = chr(0x102b)
VOWEL_SIGN_AA = chr(0x102c)
VOWEL_SIGN_I = chr(0x102d)
VOWEL_SIGN_II = chr(0x102e)
VOWEL_SIGN_U = chr(0x102f)
VOWEL_SIGN_UU = chr(0x1030)
VOWEL_SIGN_E = chr(0x1031)
VOWEL_SIGN_AI = chr(0x1032)
VOWEL_SIGN_MON_II = chr(0x1033)
VOWEL_SIGN_MON_O = chr(0x1034)
VOWEL_SIGN_E_ABOVE = chr(0x1035)
SIGN_ANUSVARA = chr(0x1036)
SIGN_DOT_BELOW = chr(0x1037)
SIGN_VISARGA = chr(0x1038)
SIGN_VIRAMA = chr(0x1039)
SIGN_ASAT = chr(0x103a)
SIGN_MEDIAL_YA = chr(0x103b)
SIGN_MEDIAL_RA = chr(0x103c)
SIGN_MEDIAL_WA = chr(0x103d)
SIGN_MEDIAL_HA = chr(0x103e)
LETTER_GREAT_SA = chr(0x103f)
DIGIT_ZERO = chr(0x1040)
DIGIT_ONE = chr(0x1041)
DIGIT_TWO = chr(0x1042)
DIGIT_THREE = chr(0x1043)
DIGIT_FOUR = chr(0x1044)
DIGIT_FIVE = chr(0x1045)
DIGIT_SIX = chr(0x1046)
DIGIT_SEVEN = chr(0x1047)
DIGIT_EIGHT = chr(0x1048)
DIGIT_NINE = chr(0x1049)
SIGN_LITTLE_SECTION = chr(0x104a)
SIGN_SECTION = chr(0x104b)
SYMBOL_LOCATIVE = chr(0x104c)
SYMBOL_COMPLETED = chr(0x104d)
SYMBOL_AFOREMENTIONED = chr(0x104e)
SYMBOL_GENITIVE = chr(0x104f)

ismyanmar = lambda c: (c >= LETTER_KA and c <= SYMBOL_GENITIVE)  # noqa
ismyconsonant = lambda c: (c >= LETTER_KA and c <= LETTER_A) or c == LETTER_U # noqa
ismymedial = lambda c: (c >= SIGN_MEDIAL_YA and c <= SIGN_MEDIAL_HA)  # noqa
ismyvowel = lambda c: (c >= VOWEL_SIGN_TALL_AA and c <= VOWEL_SIGN_AI)  # noqa
ismytone = lambda c: (c == SIGN_DOT_BELOW or c == SIGN_VISARGA)  # noqa
ismydigit = lambda c: (c >= DIGIT_ZERO and c <= DIGIT_NINE)  # noqa
ismypunct = lambda c: (c == SIGN_LITTLE_SECTION or c == SIGN_SECTION)  # noqa
ismydiac = lambda c: (ismyvowel(c) or ismymedial(c) or ismytone(c) or c == SIGN_ANUSVARA or c == SIGN_ASAT) # noqa
ismyindependvowel = lambda c: (c >= LETTER_I and c <= LETTER_E) or c == LETTER_O or c == LETTER_AU # noqa
ismyindependsymbol = lambda c: (c >= SYMBOL_LOCATIVE and c <= SYMBOL_GENITIVE) # noqa
ismyletter = lambda c: (ismyconsonant(c) or ismyindependvowel(c) or c == SYMBOL_AFOREMENTIONED) # noqa
ismymark = lambda c:(ismymedial(c) or ismyvowel(c) or (c >= SIGN_ANUSVARA and c <= SIGN_ASAT)) # noqa


def MorphoSyllableBreak(text, encoding):
    """
    Return an iterable of morphological / visual syllables in text.

    >>> from myanmar.encodings import UnicodeEncoding
    >>> slb = list(MorphoSyllableBreak("အကြွေးပေး", UnicodeEncoding()))
    >>> list(s['syllable'] for s in slb)
    ['အ', 'ကြွေး', 'ပေး']
    >>> slb[2]
    {'syllable': 'ပေး', 'consonant': 'ပ', 'eVowel': 'ေ', 'visarga': 'း'}
    """
    if not isinstance(encoding, encodings.BaseEncoding):
        raise TypeError(encoding + "is not a valid encoding")

    start = 0

    while start < len(text):
        match = encoding.morphologic_pattern.search(text, start)

        if not match:
            syllable = {'syllable': text[start:]}
            start = len(text)
        elif start < match.start():
            # unmached text (aka non-Burmese characters)
            syllable = {'syllable': text[start:match.start()]}
            start = match.start()
        else:
            # no unmatched text
            syllable = {k: v for k, v in match.groupdict().items() if v}
            start = match.end()

        yield syllable

    raise StopIteration


def PhonemicSyllableBreak(text, encoding):
    """
    Return an iterable of phonemic syllables in text.

    >>> from myanmar.encodings import UnicodeEncoding
    >>> slb = list(PhonemicSyllableBreak("သီးပင်အိုင်", UnicodeEncoding()))
    >>> list(s['syllable'] for s in slb)
    ['သီး', 'ပင်', 'အိုင်']
    >>> slb[0]
    {'syllable': 'သီး', 'consonant': 'သ', 'iVowel': 'ီ', 'visarga': 'း'}
    """
    if not isinstance(encoding, encodings.BaseEncoding):
        raise TypeError(encoding + "is not a valid encoding")

    start = 0

    while start < len(text):
        match = encoding.phonemic_pattern.search(text, start)

        if not match:
            syllable = {'syllable': text[start:]}
            start = len(text)
        elif start < match.start():
            # unmached text (aka non-Burmese characters)
            syllable = {'syllable': text[start:match.start()]}
            start = match.start()
        else:
            # no unmatched text
            syllable = {k: v for k, v in match.groupdict().items() if v}
            start = match.end()

        yield syllable

    raise StopIteration
