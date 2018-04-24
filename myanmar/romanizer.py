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
import json
import pkgutil

from myanmar.encodings import UnicodeEncoding
from myanmar.language import PhonemicSyllableBreak
from myanmar.language import SIGN_ASAT, SIGN_VIRAMA


def romanize(string, system, encoding=UnicodeEncoding()):
    """
    Transliterate Burmese text with latin letters.

    >>> romanize("ဟက်ဟက်ပက်ပက်ရယ်", BGN_PCGN)
    'het-hetpetpetyè'
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


class BGN_PCGN():
    table = json.loads(
        pkgutil.get_data('myanmar', 'data/bgn-pcgn.json').decode('utf-8')
    )
    vowels = 'aeèioôu'

    @classmethod
    def normalize(cls, roman, prev):
        roman = cls.skip_a_if_followed_by_vowel(roman)
        roman = cls.add_a_if_novowel(roman)

        if prev:
            roman = cls.change_ka_to_ga(roman, prev)
            roman = cls.change_sa_to_za(roman, prev)
            roman = cls.change_pa_to_ba(roman, prev)
            roman = cls.change_ta_to_da(roman, prev)
            roman = cls.add_hyphen_if_vowel_start(roman, prev)
            roman = cls.add_hyphen_for_ng_ny(roman, prev)
            roman = cls.add_hyphen_for_ht(roman, prev)

        return roman

    @classmethod
    def skip_a_if_followed_by_vowel(cls, roman):
        if roman.startswith('a') and cls.has_vowel(roman[1:]):
            roman = roman[1:]
        return roman

    @classmethod
    def add_a_if_novowel(cls, roman):
        if not cls.has_vowel(roman):
            roman = roman + 'a'
        return roman

    @classmethod
    def change_ka_to_ga(cls, roman, prev):
        # change ka to ga after vowel sound
        if roman.startswith('k') and cls.ends_with_vowel(prev):
            roman = 'g' + roman[1:]
        return roman

    @classmethod
    def change_sa_to_za(cls, roman, prev):
        # change sa to za after vowel sound
        if roman.startswith('s') and cls.ends_with_vowel(prev):
            roman = 'z' + roman[1:]
        return roman

    @classmethod
    def change_pa_to_ba(cls, roman, prev):
        # change pa to ba after vowel sound
        if roman.startswith('p') and cls.ends_with_vowel(prev):
            roman = 'b' + roman[1:]
        return roman

    @classmethod
    def change_ta_to_da(cls, roman, prev):
        # change ta to da after vowel sound
        startswitht = roman.startswith('t') and not roman.startswith('th')
        if startswitht and cls.ends_with_vowel(prev):
            roman = 'd' + roman[1:]
        return roman

    @classmethod
    def add_hyphen_if_vowel_start(cls, roman, prev):
        # add hyphen if started with a vowel
        if roman[0] in cls.vowels and not prev[-1].isspace():
            roman = '-' + roman
        return roman

    @classmethod
    def add_hyphen_for_ng_ny(cls, roman, prev):
        # to avoid confusion for ng / n-g & ny / n-y
        if roman[0] in 'gy' and prev[-1] == 'n':
            roman = '-' + roman
        return roman

    @classmethod
    def add_hyphen_for_ht(cls, roman, prev):
        # to avoid confusion for ht / h-t
        if roman[0] == 'h' and prev[-1] == 't':
            roman = '-' + roman
        return roman

    @classmethod
    def ends_with_vowel(cls, roman):
        return roman[-1] in 'aeioun' or roman.endswith('ng')

    @classmethod
    def has_vowel(cls, roman):
        # if any of cls.vowels  exists in roman
        return any(roman.find(v) != -1 for v in cls.vowels)


class IPA():
    table = json.loads(
        pkgutil.get_data('myanmar', 'data/ipa.json').decode('utf-8')
    )
    vowels = 'aáeèioóôu'

    @classmethod
    def normalize(cls, ipa, prev):
        ipa = ipa.replace('kj', 'tɕ')
        ipa = ipa.replace('kʰj', 'tɕʰ')
        ipa = ipa.replace('ɡj', 'dʑ')
        ipa = ipa.replace('j̥', 'ʃ')
        ipa = ipa.replace('ŋ̥', 'ŋ̊')
        ipa = ipa.replace('ŋj', 'ɲ')
        if prev:
            ipa = cls.add_ə(ipa, prev)
            ipa = cls.change_k_to_g(ipa, prev)
            ipa = cls.change_s_to_z(ipa, prev)
            ipa = cls.change_p_to_b(ipa, prev)
            ipa = cls.change_t_to_d(ipa, prev)
        return ipa

    @classmethod
    def add_ə(cls, ipa, prev):
        print('ipa:', ipa)
        print('prev:', prev)
        prev_len = 0
        if prev[-1] == 'ʰ' and len(prev[-2]) == 1:
            prev_len = 1
        if len(prev) == 1 or prev_len == 1:
            ipa = 'ə' + ipa
        return ipa

    @classmethod
    def change_k_to_g(cls, ipa, prev):
        # change k to g after vowel sound
        if ipa.startswith('k') and cls.ends_with_vowel(prev):
            ipa = 'g' + ipa[1:]
        return ipa

    @classmethod
    def change_s_to_z(cls, ipa, prev):
        # change s to z after vowel sound
        if ipa.startswith('s') and cls.ends_with_vowel(prev):
            ipa = 'z' + ipa[1:]
        return ipa

    @classmethod
    def change_p_to_b(cls, ipa, prev):
        # change pa to ba after vowel sound
        if ipa.startswith('p') and cls.has_vowel(ipa):
            ipa = 'b' + ipa[1:]
        return ipa

    @classmethod
    def change_t_to_d(cls, ipa, prev):
        # change t to d after vowel sound
        startswitht = ipa.startswith('t') and not ipa.startswith('th')
        if startswitht and cls.ends_with_vowel(prev):
            ipa = 'd' + ipa[1:]
        return ipa

    @classmethod
    def ends_with_vowel(cls, ipa):
        return ipa[-1] in 'aàeioun' or ipa.endswith('ng')

    @classmethod
    def has_vowel(cls, ipa):
        # if any of cls.vowels  exists in IPA
        return any(ipa.find(v) != -1 for v in cls.vowels)
