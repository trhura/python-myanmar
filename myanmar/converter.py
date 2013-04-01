import os.path
import codecs
import json

class BaseEncoding (object):

    def __init__ (self, jsonFile=None):
        """
        """
        self.mappings = self.load_json (jsonFile)
        self.mappings["diacritics"] = {}
        for diac in ["yapin", "yayit", "wasway", "hatoh",
                     "eVowel", "iVowel", "uVowel", "anusvara",
                     "aaVowel", "dot_below", "asat", "visarga"]:
            self.mappings["diacritics"].update (self.mappings[diac])

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
        self.syllable_pattern = ""
        super ().__init__(*args, **kwargs)


class ZawgyiEncoding (BaseEncoding):
    def __init__ (self, *args, **kwargs):
        self.syllable_pattern = ""
        super ().__init__(*args, **kwargs)

def main  ():
    uni = UnicodeEncoding ('data/unicode.json')
    zgy = ZawgyiEncoding ('data/zawgyi.json')

    import pprint
    pprint.pprint (uni.mappings)

if __name__ == "__main__":
    main ()
