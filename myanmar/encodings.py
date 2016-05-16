import json
import re
import os

class BaseEncoding ():

    def __init__ (self):
        """
        """
        # get json file name dynamically from class name
        name = self.__class__.__name__
        name = name[:name.find('Encoding')].lower() + '.json'
        _ROOT = os.path.dirname (os.path.abspath (__file__))
        self.json_data = self.load_json (os.path.join(_ROOT, 'data', name))

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
        #print (self.get_pattern () + '\n')
        return re.compile (self.get_pattern(), re.UNICODE)

    def get_pattern (self):
        def build_pattern (pattern):
            if isinstance (pattern, str):
                node = pattern
                #or_expr = "|".join(["--%s--(%s)" %(x, x.encode ('unicode_escape')) \
                #for x in sorted(self.json_data[node].values (), reverse=True, key= lambda s: len(s)) if x])
                or_expr = "|".join(set([x for x in sorted(self.json_data[node].values (),
                                                          key=lambda s: len(s),
                                                          reverse=True)
                                        if x]))
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
