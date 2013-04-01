import os.path
import json

class BaseEncoding (object):

    def __init__ (self, jsonFile=None):
        """
        """
        self.mappings = self.load_json (jsonFile)

        self.mappings["pre-diacritics"] = {}
        for i in ["eVowel", "yayit", "kinzi"]:
            self.mappings["pre-diacritics"].update (self.mappings[i])
        self.mappings["post-diacritics"] = {}
        for i in ["stack", "yapin", "iVowel", "uVowel", "anusvara",
                  "aaVowel", "dot_below", "asat", "visarga"]:
            self.mappings["post-diacritics"].update (self.mappings[i])

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

class UnicodeEncoding (BaseEncoding):
    def __init__ (self, *args, **kwargs):
        self.syllable_pattern = []
        super ().__init__(*args, **kwargs)

class ZawgyiEncoding (BaseEncoding):
    def __init__ (self, *args, **kwargs):
        self.syllable_pattern = [
            "independent",
            "digits",
            "puncts",
            "lig",
            [("pre-diacritics",), "cons", ("post-diacritics",)],
        ]
        super ().__init__(*args, **kwargs)

def main  ():
    uni = UnicodeEncoding ('data/unicode.json')
    zgy = ZawgyiEncoding ('data/zawgyi.json')

    # import pprint
    # pprint.pprint (uni.mappings)

if __name__ == "__main__":
    main ()
