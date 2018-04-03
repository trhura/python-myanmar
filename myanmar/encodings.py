# encodings.py - encodings module
# coding: utf-8
# The MIT License (MIT)
# Copyright (c) 2018 Thura Hlaing

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import re
import os
import json
import pkgutil

class BaseEncoding ():

    def __init__ (self):
        # get json file name dynamically from class name
        encname = self.__class__.__name__
        filename = encname[:encname.find('Encoding')].lower() + '.json'
        self.json_data = json.loads(pkgutil.get_data('myanmar', 'data/' + filename))

        self.reverse_table = self.get_reverse_table ()
        self.table = self.get_table ()
        self.pattern = self.get_compiled_pattern ()

    def get_table (self):
        ret = {}
        for key, value in self.json_data.items ():
            ret.update ({k: v for k, v in value.items() if v})
        return ret

    def get_reverse_table (self):
        ret = {}
        for key, value in self.json_data.items ():
            ret.update ({v: k for k, v in value.items() if v})
        return ret

    def get_compiled_pattern (self):
        return re.compile (self.get_pattern(), re.UNICODE)

    def get_pattern (self):
        def build_pattern (pattern):
            if isinstance (pattern, str):
                node = pattern
                #or_expr = "|".join(["--%s--(%s)" %(x, x.encode ('unicode_escape')) \
                #for x in sorted(self.json_data[node].values (), reverse=True, key= lambda s: len(s)) if x])
                or_expr = "|".join([x for x in sorted(set(self.json_data[node].values()),
                                                      key=len,
                                                      reverse=True)
                                        if x])
                return '(?P<' + pattern + '>'+  or_expr + ')'

            if isinstance (pattern, tuple):
                ret_list = [build_pattern (x) for x in pattern]
                if len(ret_list) > 1:
                    return '(' + "|".join (ret_list) + ')*'
                else:
                    return ret_list[0] + '*'

            if isinstance (pattern, list):
                return ''.join([build_pattern (x) for x in  pattern])

        return "(?P<syllable>"+ "|".join ([build_pattern(x) for x in self.syllable_form]) + ")"

    @classmethod
    def load_json (cls, jsonFile):
        if not jsonFile:
            raise RuntimeError ("jsonFile must not be None.")

        if not os.path.exists (jsonFile):
            raise RuntimeError ("jsonFile doesn't exists on the system.")

        with open (jsonFile, 'r') as iFile:
            data = json.load (iFile)
            return data

class UnicodeEncoding (BaseEncoding):

    def __init__ (self, *args, **kwargs):
        self.syllable_pattern = [("kinzi",), "consonant", ("stack",),
                                 ("yapin",), ("yayit",), ("wasway",), ("hatoh",),
                                 ("eVowel",), ("iVowel",), ("uVowel", "anusvara"),
                                 ("aiVowel",), ("aaVowel", "asat", "dotBelow"), ("visarga",)]
        self.syllable_form = [
            "independent",
            "digit",
            "punctuation",
            "ligature",
            self.syllable_pattern
            ]

        super ().__init__(*args, **kwargs)

class LegacyEncoding (BaseEncoding):

    def __init__ (self, *args, **kwargs):
        self.syllable_pattern  = [("eVowel",), ("yayit",), "consonant", ("kinzi",),
                                  ("stack",), ("yapin", "wasway", "hatoh",),
                                  ("iVowel", "uVowel", "anusvara", "aiVowel"),
                                  ("aaVowel", "asat", "dotBelow"), ("visarga",)]
        self.syllable_form = [
            "independent",
            "digit",
            "punctuation",
            "ligature",
            self.syllable_pattern
            ]
        super ().__init__(*args, **kwargs)

class ZawgyiEncoding (LegacyEncoding):
    pass

class WininnwaEncoding (LegacyEncoding):
    pass
