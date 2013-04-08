import os.path
import itertools
import glob
import imp
from language import *

# FIXME:
enc = imp.load_source ('encodings',
                       os.path.join (os.path.dirname (os.path.abspath (__file__)),
                                     'encodings.py'))

def get_available_encodings ():
    encodings = []
    _ROOT = os.path.dirname (os.path.abspath (__file__))
    for path in glob.glob (os.path.join (_ROOT, 'data', '*.json')):
        encodings += [os.path.splitext (os.path.basename(path))[0]]
    return encodings

def convert (text, from_encoding, to_encoding):
    """
    Take a unicode string, and convert it to from_encoding to
    to_encoding.

    Supported encodings can be obtained by get_available_encodings ()
    function.
    """
    encodings = { encoding:  getattr(enc, encoding.title() + 'Encoding') \
                  for encoding in get_available_encodings() }

    for encoding  in [from_encoding, to_encoding]:
        if not encoding in encodings:
            raise NotImplementedError ("Unsupported encoding: %s" % encoding)

    from_encoding = encodings[from_encoding]()
    to_encoding = encodings[to_encoding]()
    iterator = SyllableIter (text=text, encoding=from_encoding)

    otext = ""
    for each_syllable in iterator:
        complete_syllable = each_syllable['syllable']

        if len(each_syllable) == 1:
            # unmatched text, no need to convert
            otext += complete_syllable
            continue

        if complete_syllable in from_encoding.reverse_table:
            # Direct mapping
            key = from_encoding.reverse_table[complete_syllable]
            otext += to_encoding.table[key]
            continue

        # flattern syllable_pattern, convert to a list of tuples first
        syllable_pattern = [(x,) if isinstance(x, str) else x for x in to_encoding.syllable_pattern]
        syllable_pattern = list(itertools.chain(*syllable_pattern))

        # collect codepoints in syllable, in correct syllable order
        syllable = ""
        for each_pattern in syllable_pattern:
            print(each_syllable)
            if not each_pattern in each_syllable:
                continue

            key = from_encoding.reverse_table[each_syllable[each_pattern]]
            key = key[:key.find('_')] if '_' in key else key # remove variant suffixes

            if each_pattern == "consonant":
                if each_syllable["consonant"] == LETTER_NA:
                    key +=  choose_na_variant (each_syllable)

            if each_pattern == "yayit":
                key += choose_yayit_variant (each_syllable)

            if each_pattern == "uVowel":
                key += choose_uvowel_variant (each_syllable)

            if each_pattern == "aaVowel":
                key += choose_aavowel_variant (each_syllable)

            if each_pattern == "yapin":
                key += choose_yapin_variant (each_syllable)

            char = to_encoding.table[key]
            syllable += char

        otext += syllable

    from pprint import pprint
    #pprint (to_encoding.table)
    #pprint (from_encoding.reverse_table)
    return otext

def is_wide_consonant (char):
    WIDE_CONSONANTS = [
    LETTER_KA, LETTER_GHA, LETTER_CA, LETTER_CHA,
    LETTER_NYA, LETTER_NNA, LETTER_TA, LETTER_THA,
    LETTER_BHA, LETTER_YA, LETTER_LA, LETTER_SA,
    LETTER_HA, LETTER_A, LETTER_GREAT_SA
    ]
    return char in WIDE_CONSONANTS

def is_lower_consonant (char):
    LOWER_CONSONANTS = [
        LETTER_NYA,
    # ... more
    LETTER_NA,
    LETTER_RA,
    ]
    return char in LOWER_CONSONANTS

def has_lower_marks (syllable, filters=[]):
    MAKRS = ["stack", "wasway", "yapin",
             "yayit", "hatoh", "uVowel"]
    for mark in [m for m in MAKRS if not m in filters]:
        if mark in syllable:
            return True
    return False

def choose_na_variant (syllable):
    key = "_alt" if has_lower_marks (syllable) else ""
    return key

def choose_uvowel_variant (syllable):
    key = "_tall" if has_lower_marks (syllable, ["uVowel"]) else ""
    return key

def choose_aavowel_variant (syllable):
    _C = [LETTER_GHA, LETTER_NGA, LETTER_DA,
          LETTER_DHA, LETTER_PA, LETTER_WA]
    key = "_tall" if syllable['consonant'] in _C else ""
    return key

def choose_yayit_variant (syllable):
    key = "_wide" if is_wide_consonant(syllable['consonant']) else ""
    return key

def choose_yapin_variant (syllable):
    key = "_alt" if has_lower_marks (syllable, ["yapin"]) else ""
    return key

def main  ():
    with open ('data/test2.txt', mode='r', encoding='utf-8') as iFile:
        data = iFile.read ()
        print(convert (data, 'unicode', 'zawgyi'))

if __name__ == "__main__":
    main ()
