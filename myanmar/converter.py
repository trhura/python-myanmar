import os.path
import itertools
import glob
import imp
import sys
from myanmar.language import *
from myanmar import encodings as enc

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
    #print (from_encoding.get_pattern())

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
            key = key[:key.find('_')] if '_' in key else key # remove variant suffixes
            otext += to_encoding.table[key]
            continue

        # flattern syllable_pattern, convert to a list of tuples first
        syllable_pattern = [(x,) if isinstance(x, str) else x for x in to_encoding.syllable_pattern]
        syllable_pattern = list(itertools.chain(*syllable_pattern))

        # collect codepoints in syllable, in correct syllable order
        syllable = {}
        flags = {}

        for each_part in each_syllable.keys():
            if each_part == 'syllable': continue # skip complete syllable

            key = from_encoding.reverse_table[each_syllable[each_part]]
            key = key[:key.find('_')] if '_' in key else key # remove variant suffixes

            if each_part == "consonant":
                if key == "na":
                    key += choose_na_variant (each_syllable)

                if key == "ra":
                    key += choose_ra_variant (each_syllable)

                if key == "nnya":
                    key += choose_nnya_variant (each_syllable)

            if each_part == "yapin":
                key += choose_yapin_variant (each_syllable)

            if each_part == "yayit":
                key += choose_yayit_variant (each_syllable)

            if each_part == "uVowel":
                key += choose_uvowel_variant (each_syllable)
                flags[each_part] = key

            if each_part == "aaVowel":
                key += choose_aavowel_variant (each_syllable)

            if each_part == "dotBelow":
                key += choose_dot_below_variant (each_syllable)

            syllable[each_part] = key

        if 'uVowel' in syllable and 'hatoh' in syllable:
            del syllable['uVowel']
            syllable['hatoh'] = syllable['hatoh'] + '_' + flags['uVowel']

        if 'wasway' in syllable and 'hatoh' in syllable:
            del syllable['hatoh']
            syllable['wasway'] = syllable['wasway'] + '-' + 'hatoh'

        for each_pattern in syllable_pattern:
            if each_pattern not in syllable:
                continue

            try:
                key = syllable[each_pattern]
                otext += to_encoding.table[key]
            except Exception as e:
                print(key, syllable,file=sys.stderr)

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

def has_upper_marks (syllable, filters=[]):
    MAKRS = ["kinzi", "yapin", "iVowel",
             "aiVowel", "anusvara"]
    for mark in [m for m in MAKRS if not m in filters]:
        if mark in syllable:
            return True
    return False

def choose_ra_variant (syllable):
    key = "_alt" if "uVowel" in syllable else ""
    return key

def choose_na_variant (syllable):
    key = "_alt" if has_lower_marks (syllable) else ""
    return key

def choose_nnya_variant (syllable):
    key = "_alt" if has_lower_marks (syllable) else ""
    return key

def choose_uvowel_variant (syllable):
    key = "_tall" if has_lower_marks (syllable, ["uVowel", "hatoh"]) else ""
    return key

def choose_aavowel_variant (syllable):
    _C = [LETTER_KHA, LETTER_GHA, LETTER_NGA, LETTER_DA,
          LETTER_DHA, LETTER_PA, LETTER_WA]

    #FIXME: asat
    key = ''
    if 'asat' in syllable:
        key += '-asat'

    if syllable['consonant'] in _C:
        for c in ['yapin', 'yayit', 'wasway', 'hatoh']:
            if c in syllable:
                break
        else:
            key += '_tall'

    return key

def choose_yayit_variant (syllable):
    key = "_wide" if is_wide_consonant(syllable['consonant']) else "_narrow"
    key += "_lower" if has_lower_marks (syllable, ["yayit", "uVowel"]) else ""
    key += "_upper" if has_upper_marks (syllable, ["yayit"]) else ""
    return key

def choose_yapin_variant (syllable):
    key = "_alt" if has_lower_marks (syllable, ["yapin", "uVowel"]) else ""
    return key

def choose_dot_below_variant (syllable):
    key = ""

    if syllable['consonant'] == LETTER_NA:
        key += "_alt"
    elif syllable['consonant'] == LETTER_RA:
        key += "_alt_alt"
    elif "uVowel" in syllable:
        key += "_alt_alt" if 'yayit' in syllable else '_alt'
    elif "yapin" in syllable:
        key += "_alt"
    elif  "wasway" in syllable:
        key += "_alt_alt"

    return key

def main  ():
    pass

if __name__ == "__main__":
    main ()
