#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is very
"""
import re
from codepoints import *

irange = lambda x,y,z=1: range(ord(x), ord(y)+1,z)

digits_     = [ unichr(x) for x in irange (DIGIT_ZERO, DIGIT_NINE)]
all_        = [ unichr(x) for x in irange (LETTER_KA, SYMBOL_GENITIVE)]
consonants_ = [ unichr(x) for x in irange (LETTER_KA, LETTER_A)]
medials_    = [ unichr(x) for x in irange (CONSONANT_SIGN_MEDIAL_YA, CONSONANT_SIGN_MEDIAL_HA)]
vowels_     = [ unichr(x) for x in irange (VOWEL_SIGN_TALL_AA, VOWEL_SIGN_AI)]
tones_      = [SIGN_DOT_BELOW, SIGN_VISARGA]
diacs_      = [SIGN_ASAT, SIGN_ANUSVARA]  + vowels_ + medials_ + tones_
puncts_     = [SIGN_SECTION, SIGN_LITTLE_SECTION]
indepvwls_  = [ unichr(x) for x in irange(LETTER_I, LETTER_E)] + [LETTER_O, LETTER_AU]
indepsyms_  = [ unichr(x) for x in irange(SYMBOL_LOCATIVE, SYMBOL_GENITIVE)]

def ismyanmar (wc):
    return (wc >= LETTER_KA and wc <= SYMBOL_GENITIVE)

def ismyconsonant (wc):
    return ((wc >= LETTER_KA) and (wc <= LETTER_A)) # wc == LETTER_GREAT_SA)

def ismymedial (wc):
    return (wc >= CONSONANT_SIGN_MEDIAL_YA) and (wc <= CONSONANT_SIGN_MEDIAL_HA)

def ismyvowel (wc):
    return ((wc >= VOWEL_SIGN_TALL_AA) and (wc <= VOWEL_SIGN_AI))

def ismytone (wc):
    return (wc == SIGN_DOT_BELOW or wc == SIGN_VISARGA)

def ismydiac (wc):
    return (ismyvowel (wc) or ismymedial (wc) or ismytone (wc) or
            wc == SIGN_ANUSVARA or wc == SIGN_ASAT)

def ismydigit (wc):
    return (wc >= DIGIT_ZERO  and wc <= DIGIT_NINE)

def ismypunct (wc):
    return (wc == SIGN_LITTLE_SECTION or wc == SIGN_SECTION)

def ismyindependvowel (wc):
    return (wc >= LETTER_I and wc <= LETTER_E) or wc == LETTER_O or wc == LETTER_AU

def ismyindependsymbol (wc):
    return (wc >= SYMBOL_LOCATIVE and
            wc <= SYMBOL_GENITIVE)

def ismyletter (wc):
    return (ismyconsonant (wc) or
            ismyindependvowel (wc) or
            wc == SYMBOL_AFOREMENTIONED)

def ismymark (wc):
    return (ismymedial (wc) or
            ismyvowel  (wc) or
            (wc >= SIGN_ANUSVARA and wc<= SIGN_ASAT))

def to_unicode_repr (string):
    x = [ r"\u%x" %ord(s) for s in string.decode("utf-8")]
    return  "".join (x)

class ClusterIter (object):

    def __init__ (self, string):
        #self.syllable_pattern = re.compile (self._build_pattern())
        if isinstance (string, unicode):
            self.string = string

        elif isinstance (string, str):
            self.string = string.decode ('utf8')
            #self.string  = string #if isinstance (string, unicode) else string.decode ('utf-8')
        else:
            raise TypeError ('string must be an instance of either unicode or str.')

        self.pos = 0
        self.len = len(self.string)

    def __iter__ (self):
        return self

    def next (self):
        if not (self.pos < self.len):
            raise StopIteration

        i = j = self.pos

        if not ismyanmar  (self.string[i]):
            while (j < self.len and not ismyanmar (self.string[j])):
                j += 1
                self.pos = j
                return self.string[i:j]

        if (i < self.len and not ismyletter (self.string[i])):
            # Find the first consonant
            if (ismydigit(self.string[i]) or
                ismypunct(self.string[i]) or
                ismyindependsymbol (self.string[i])):
                j = i + 1
                self.pos = j
                return self.string[i:j]
            while (j < self.len and not ismyletter (self.string[j])):
                j += 1
            self.pos = j
            return self.string[i:j]

        j = i + 1;
        devowelized = True

        while (devowelized):
            devowelized = False
            while (j < self.len and not ismyletter (self.string[j])):
                # find the next consonant
                if (not ismyanmar (self.string[j]) or
                    ismydigit(self.string[j]) or
                    ismypunct(self.string[j]) or
                    ismyindependsymbol (self.string[j])):
                    self.pos = j
                    return self.string[i:j]
                j += 1

            if (j == self.len):
                self.pos = j
                return self.string[i:j]

            if (self.string[j-1] == SIGN_VIRAMA):
                # preceded by virama
                j += 1;
                devowelized = True

            if ((j+1 < self.len) and self.string[j+1] == SIGN_VIRAMA ):
                # followed by virama
                j += 3;
                devowelized = True

            # Checks whether the consonant is followed by asat
            k = j;
            while (k + 1 < self.len and ismydiac (self.string[k+1])):
                if (self.string[k + 1] == VOWEL_SIGN_AA) or \
                    (self.string[k + 1] == VOWEL_SIGN_TALL_AA):
                    break

                if (self.string[k + 1] == SIGN_ASAT):
                    devowelized = True
                    j = k + 1
                    break
                k += 1

        self.pos = j
        return self.string[i:j]
