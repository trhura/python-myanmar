#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO
"""

LETTER_KA					= unichr(0x1000)
LETTER_KHA					= unichr(0x1001)
LETTER_GA					= unichr(0x1002)
LETTER_GHA					= unichr(0x1003)
LETTER_NGA					= unichr(0x1004)
LETTER_CA					= unichr(0x1005)
LETTER_CHA					= unichr(0x1006)
LETTER_JA					= unichr(0x1007)
LETTER_JHA					= unichr(0x1008)
LETTER_NYA					= unichr(0x1009)
LETTER_NNYA					= unichr(0x100a)
LETTER_TTA					= unichr(0x100b)
LETTER_TTHA					= unichr(0x100c)
LETTER_DDA					= unichr(0x100d)
LETTER_DDHA					= unichr(0x100e)
LETTER_NNA					= unichr(0x100f)
LETTER_TA					= unichr(0x1010)
LETTER_THA					= unichr(0x1011)
LETTER_DA					= unichr(0x1012)
LETTER_DHA					= unichr(0x1013)
LETTER_NA					= unichr(0x1014)
LETTER_PA					= unichr(0x1015)
LETTER_PHA					= unichr(0x1016)
LETTER_BA					= unichr(0x1017)
LETTER_BHA					= unichr(0x1018)
LETTER_MA					= unichr(0x1019)
LETTER_YA					= unichr(0x101a)
LETTER_RA					= unichr(0x101b)
LETTER_LA					= unichr(0x101c)
LETTER_WA					= unichr(0x101d)
LETTER_SA					= unichr(0x101e)
LETTER_HA					= unichr(0x101f)
LETTER_LLA					= unichr(0x1020)
LETTER_A					= unichr(0x1021)
LETTER_SHAN_A				= unichr(0x1022)
LETTER_I					= unichr(0x1023)
LETTER_II					= unichr(0x1024)
LETTER_U					= unichr(0x1025)
LETTER_UU					= unichr(0x1026)
LETTER_E					= unichr(0x1027)
LETTER_MON_E				= unichr(0x1028)
LETTER_O					= unichr(0x1029)
LETTER_AU					= unichr(0x102a)
VOWEL_SIGN_TALL_AA 			= unichr(0x102b)
VOWEL_SIGN_AA				= unichr(0x102c)
VOWEL_SIGN_I				= unichr(0x102d)
VOWEL_SIGN_II				= unichr(0x102e)
VOWEL_SIGN_U				= unichr(0x102f)
VOWEL_SIGN_UU				= unichr(0x1030)
VOWEL_SIGN_E				= unichr(0x1031)
VOWEL_SIGN_AI				= unichr(0x1032)
VOWEL_SIGN_MON_II 			= unichr(0x1033)
VOWEL_SIGN_MON_O 			= unichr(0x1034)
VOWEL_SIGN_E_ABOVE 			= unichr(0x1035)
SIGN_ANUSVARA				= unichr(0x1036)
SIGN_DOT_BELOW				= unichr(0x1037)
SIGN_VISARGA				= unichr(0x1038)
SIGN_VIRAMA					= unichr(0x1039)
SIGN_ASAT					= unichr(0x103a)
CONSONANT_SIGN_MEDIAL_YA 	= unichr(0x103b)
CONSONANT_SIGN_MEDIAL_RA 	= unichr(0x103c)
CONSONANT_SIGN_MEDIAL_WA 	= unichr(0x103d)
CONSONANT_SIGN_MEDIAL_HA 	= unichr(0x103e)
LETTER_GREAT_SA 			= unichr(0x103f)
DIGIT_ZERO					= unichr(0x1040)
DIGIT_ONE					= unichr(0x1041)
DIGIT_TWO					= unichr(0x1042)
DIGIT_THREE					= unichr(0x1043)
DIGIT_FOUR					= unichr(0x1044)
DIGIT_FIVE					= unichr(0x1045)
DIGIT_SIX					= unichr(0x1046)
DIGIT_SEVEN					= unichr(0x1047)
DIGIT_EIGHT					= unichr(0x1048)
DIGIT_NINE					= unichr(0x1049)
SIGN_LITTLE_SECTION 		= unichr(0x104a)
SIGN_SECTION				= unichr(0x104b)
SYMBOL_LOCATIVE 			= unichr(0x104c)
SYMBOL_COMPLETED 			= unichr(0x104d)
SYMBOL_AFOREMENTIONED 		= unichr(0x104e)
SYMBOL_GENITIVE 			= unichr(0x104f)

irange = lambda x,y,z=1: range(ord(x), ord(y)+1,z)

digits     = [ unichr(x) for x in irange (DIGIT_ZERO, DIGIT_NINE)]
all        = [ unichr(x) for x in irange (LETTER_KA, SYMBOL_GENITIVE)]
consonants = [ unichr(x) for x in irange (LETTER_KA, LETTER_A)]
medials    = [ unichr(x) for x in irange (CONSONANT_SIGN_MEDIAL_YA, CONSONANT_SIGN_MEDIAL_HA)]
vowels     = [ unichr(x) for x in irange (VOWEL_SIGN_TALL_AA, VOWEL_SIGN_AI)]
tones      = [SIGN_DOT_BELOW, SIGN_VISARGA]
diacs      = [SIGN_ASAT, SIGN_ANUSVARA]  + vowels + medials + tones
puncts     = [SIGN_SECTION, SIGN_LITTLE_SECTION]
indepvwls  = [ unichr(x) for x in irange(LETTER_I, LETTER_E)] + [LETTER_O, LETTER_AU]
indepsyms  = [ unichr(x) for x in irange(SYMBOL_LOCATIVE, SYMBOL_GENITIVE)]

def ismyanmar (wc):
    return (wc >= LETTER_KA and wc <= SYMBOL_GENITIVE)

def ismyconsonant (wc):
    return ((wc >= LETTER_KA) and (wc <= LETTER_A))

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

def normalize (string):
    def try_next (func, iter_, i):
        try:
            return func(iter_[i+1])
        except IndexError, e:
            #print str(e)
            return False

    def try_previous (func, iter_, i):
        try:
            return func(iter_[i-1])
        except IndexError, e:
            #print str(e)
            return False

    string = string.replace (LETTER_U + VOWEL_SIGN_II,
                             LETTER_UU)
    string = string.replace (DIGIT_FOUR + LETTER_NGA,
                             SYMBOL_AFOREMENTIONED + LETTER_NGA)

    for i, ch in enumerate(string):
        for x, y in [(DIGIT_ZERO, LETTER_WA),
                     (DIGIT_SEVEN, LETTER_RA)]:
            if ch == x and not (try_previous (ismydigit, string, i) or
                                try_next (ismydigit, string ,i)):
                string = string[:i] + y + string[i+1:]
                #print "replacing %s->%s", x.encode ('utf-8'), y.encode ('utf-8')

        if ch == LETTER_U and try_next (ismydiac, string, i):
            #print type(string), string[i],
            string = string[:i] + LETTER_NYA + string[i+1:]

    return string

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

            if ((j-1 > 0) and self.string[j-1] == SIGN_VIRAMA):
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
