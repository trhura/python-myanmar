import os.path
import json
import re

class BaseEncoding (object):

    def __init__ (self, jsonFile=None):
        """
        """
        self.mappings = self.load_json (jsonFile)
        self.update_mappings ()
        self.pattern = self.get_pattern ()
        print (self.pattern)

    def get_pattern (self):
        def build_pattern (pattern):
            if isinstance (pattern, str):
                node = pattern
                return '(?P<' + pattern + '>'+ "|".join([x for x in sorted(self.mappings[node].values ())]) + ')'
            if isinstance (pattern, tuple):
                node = pattern[0]
                return '(?P<' + pattern[0] + '>' + "|".join([x for x in self.mappings[node].values ()]) + ')*'
            if isinstance (pattern, list):
                node = pattern
                return '('+ ''.join([build_pattern (x) for x in  node]) + ')'

        return "|".join ([build_pattern(x) for x in self.syllable_pattern])

    def load_json (self, jsonFile):
        if not jsonFile:
            raise RuntimeError ("jsonFile must not be None.")

        if not os.path.exists (jsonFile):
            raise RuntimeError ("jsonFile doesn't exists on the system.")

        with open (jsonFile, 'r') as iFile:
            mappings = json.load (iFile)
            return mappings

    def update_mappings (self): pass

class UnicodeEncoding (BaseEncoding):
    def __init__ (self, *args, **kwargs):
        self.syllable_pattern = [
            "independent",
            "digits",
            "puncts",
            [("pre_diacritics",), "cons", ("post_diacritics",)],
            ]
        super ().__init__(*args, **kwargs)

    def update_mappings (self):
        self.mappings["pre_diacritics"] = {}
        for i in ["kinzi"]:
            self.mappings["pre_diacritics"].update (self.mappings[i])

        self.mappings["post_diacritics"] = {}
        for i in ["stack", "yayit", "yapin", "wasway", "hatoh", "eVowel", "iVowel",
                  "uVowel", "anusvara", "aaVowel", "dot_below", "asat", "visarga"]:
            self.mappings["post_diacritics"].update (self.mappings[i])

class ZawgyiEncoding (BaseEncoding):
    def __init__ (self, *args, **kwargs):
        self.syllable_pattern = [
            "independent",
            "digits",
            "puncts",
            "lig",
            [("pre_diacritics",), "cons", ("post_diacritics",)],
        ]
        super ().__init__(*args, **kwargs)

    def update_mappings (self):
        self.mappings["pre_diacritics"] = {}
        for i in ["eVowel", "yayit", "kinzi"]:
            self.mappings["pre_diacritics"].update (self.mappings[i])

        self.mappings["post_diacritics"] = {}
        for i in ["stack", "yapin", "wasway", "hatoh", "iVowel", "uVowel",
                  "anusvara", "aaVowel", "dot_below", "asat", "visarga"]:
            self.mappings["post_diacritics"].update (self.mappings[i])

class SyllableIter ():

    def __init__ (self, text="", encoding=UnicodeEncoding('data/unicode.json')):
        self.text = text
        self.pattern  = re.compile (encoding.get_pattern (), re.UNICODE)

    def __iter__ (self):
        return self

    def __next__ (self):
        for match in self.pattern.finditer (self.text):
            return match.start(), match.end()


def main  ():
    uni = UnicodeEncoding ('data/unicode.json')
    zgy = ZawgyiEncoding ('data/zawgyi.json')

    with open ('data/test.txt', mode='r', encoding='utf-8') as iFile:
        data = iFile.read ()
        itr = SyllableIter (text=data, encoding=zgy)

        print (data, itr.pattern.pattern)

    # import pprint
    # pprint.pprint (uni.mappings)

if __name__ == "__main__":
    main ()
