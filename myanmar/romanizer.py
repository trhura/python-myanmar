# romanizer.py - transliteration module
# coding: utf-8
# The MIT License (MIT)
# Copyright (c) 2018 Thura Hlaing

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

# import json
# import pkgutil

# from myanmar.language import myanmar_phonemic_iter

# class Romanizer():
#     data = None  # subclass needs to override this

#     @staticmethod
#     def romanize(cls_type, string):
#         if not issubclass(cls_type, Romanizer):
#             raise TypeError("cls type must be a subclass of Romanizer.")
#         return cls_type.romanize_(string)

#     @classmethod
#     def romanize_(cls, string):
#         romans = []
#         # maxkeylen = max(len(k) for k in cls.data.keys())
#         for phoneme in myanmar_phonemic_iter(string):
#             romanstr = ""
#             curpos = 0
#             print(phoneme)
#             while curpos < len(phoneme):
#                 lookuplen = len(phoneme)
#                 while lookuplen > 0:
#                     lookupstr = phoneme[curpos:lookuplen]
#                     # str(lookuplen)+ phoneme[curpos:lookuplen]+ romanstr)
#                     if lookupstr in cls.data:
#                         romanstr += cls.data[lookupstr]
#                         curpos += (lookuplen - curpos)
#                         break
#                     else:
#                         lookuplen -= 1
#                 else:
#                     # sys.stderr.write("Unable romanize " + phoneme[curpos] )
#                     romanstr += phoneme[curpos]
#                     curpos += 1
#             romans.append(romanstr)

#         return cls.join_(romans)

#     @classmethod
#     def join_(cls, romans):
#         return "".join(romans)

# class BGN_PCGN(Romanizer):
#     data = json.loads(
#         pkgutil.get_data('myanmar', 'data/bgn-pcgn.json').decode('utf-8')
#     )
#     vowels = 'aeèioôu'

#     @classmethod
#     def join_(cls, romans):
#         new_romans = []
#         for i, roman in enumerate(romans):
#             roman = cls.handle_letter_a(roman)
#             roman = cls.add_vowel_a_if_necessary(roman)

#             if roman.startswith('k') and i > 0:
#                 if new_romans[i - 1][
#                     -1
#                 ] in 'aeioun' or new_romans[i - 1].endswith('ng'):
#                     # change ka to ga after vowel sound
#                     roman = 'g' + roman[1:]

#             if roman.startswith('s') and i > 0:
#                 if new_romans[i - 1][
#                     -1
#                 ] in 'aeioun' or new_romans[i - 1].endswith('ng'):
#                     # change sa to za after vowel sound
#                     roman = 'z' + roman[1:]

#             if roman.startswith('p') and i > 0:
#                 if new_romans[i - 1][
#                     -1
#                 ] in 'aeioun' or new_romans[i - 1].endswith('ng'):
#                     # change pa to ba after vowel sound
#                     roman = 'b' + roman[1:]

#             if roman.startswith('t') and not roman.startswith('th') and i > 0: # noqa
#                 if new_romans[i - 1][
#                     -1
#                 ] in 'aeioun' or new_romans[i - 1].endswith('ng'):
#                     # change ta to da after vowel sound
#                     roman = 'd' + roman[1:]

#             if roman[
#                 0
#             ] in cls.vowels and i > 0 and not new_romans[i - 1][-1].isspace(): # noqa
#                 # add hyphen if started with a vowel
#                 roman = '-' + roman

#             if roman[0] in 'gy' and i > 0 and new_romans[i - 1][-1] == 'n':
#                 # to differetiate ng & ny
#                 roman = '-' + roman

#             if roman[0] == 'h' and i > 0 and new_romans[i - 1][-1] == 't':
#                 roman = '-' + roman

#             new_romans.append(roman)

#         # print(new_romans)
#         return "".join(new_romans)

#     @classmethod
#     def handle_letter_a(cls, roman):
#         if roman.startswith('a') and cls.has_vowel(roman[1:]):
#             return roman[1:]
#         return roman

#     @classmethod
#     def has_vowel(cls, roman):
#         for v in cls.vowels:
#             # print type(v), type(roman)
#             if roman.find(v) != -1:
#                 return True
#         return False

#     @classmethod
#     def add_vowel_a_if_necessary(cls, roman):
#         if cls.has_vowel(roman):
#             return roman
#         else:
#             return roman + 'a'
