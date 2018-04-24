# bgp_pgcn.py - BGP/PGCN transliteration module
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

import json
import pkgutil


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
