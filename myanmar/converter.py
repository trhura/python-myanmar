import os.path
import itertools
import glob
import imp
from language import SyllableIter

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
            if not each_pattern in each_syllable:
                continue

            key = from_encoding.reverse_table[each_syllable[each_pattern]]
            char = to_encoding.table[key]

            if each_pattern == "yayit":
                char = choose_yayit (each_syllable, to_encoding.table)
            syllable += char

        otext += syllable

    from pprint import pprint
    #pprint (to_encoding.table)
    #pprint (from_encoding.reverse_table)
    return otext

def choose_yayit (syllable, table):
    return table['yayit']

def main  ():
    with open ('data/test2.txt', mode='r', encoding='utf-8') as iFile:
        data = iFile.read ()
        print(convert (data, 'unicode', 'zawgyi'))

if __name__ == "__main__":
    main ()
