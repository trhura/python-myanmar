# mlc.py - mlc transliteration module
# coding: utf-8
# The MIT License (MIT)
# Credit for IPA rules - Wikipedia, LionSlayer ...
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


class MLC():
    table = json.loads(
        pkgutil.get_data('myanmar', 'data/mlc.json').decode('utf-8')
    )
    vowels = 'āiīuūeao'

    @classmethod
    def normalize(cls, roman, prev):
        roman = cls.skip_a_if_followed_by_vowel(roman)
        roman = cls.add_a_if_novowel(roman)
        roman = cls.check_a_that_with_vowel(roman)
        if prev:
            roman = cls.change_ka_to_ga(roman, prev)
            roman = cls.change_sa_to_za(roman, prev)
            roman = cls.change_pa_to_ba(roman, prev)
            roman = cls.change_ta_to_da(roman, prev)

        return roman

    @classmethod
    def check_a_that_with_vowel(cls, roman):
        for index, value in enumerate(roman):
            if value == 'ʻ' and index != len(roman)-1:
                arr = list(roman)
                if arr[index+1] == "a":
                    arr[index]=''
                    arr[index-1], arr[index+1] = arr[index+1], arr[index-1]
                    roman = "".join(arr);
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
    def change_ka_to_ga(cls, roman, prev):
        # change ka to ga after vowel sound
        if roman.startswith('k') and cls.ends_with_vowel(prev):
            roman = 'g' + roman[1:]
        return roman

    @classmethod
    def ends_with_vowel(cls, roman):
        return roman[-1] in 'aeioun' or roman.endswith('ng')

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
    def has_vowel(cls, roman):
        # if any of cls.vowels  exists in roman
        return any(roman.find(v) != -1 for v in cls.vowels)
