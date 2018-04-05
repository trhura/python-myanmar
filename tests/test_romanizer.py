#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from myanmar.romanizer import romanize, BGN_PCGN


def test_bgp_pcgn_romanizer():
    assert romanize('ကို', BGN_PCGN) == "ko"
    assert romanize('အက', BGN_PCGN) == "aga"
    assert romanize('မဒမ', BGN_PCGN) == "madama"
    assert romanize('သာငယ်', BGN_PCGN) == 'thangè'
    assert romanize('ပြစင်', BGN_PCGN) == 'pyazin'
    assert romanize('အကာ', BGN_PCGN) == 'aga'
    assert romanize('အိုဘဲ့', BGN_PCGN) == 'obè'
    assert romanize("အပ်", BGN_PCGN) == "at"
    assert romanize("မအူ", BGN_PCGN) == "ma-u"
    assert romanize("သီးပင်အိုင်", BGN_PCGN) == 'thibin-aing'
    assert romanize("ဩဘာ", BGN_PCGN) == "awba"
    assert romanize("ဧဏီ", BGN_PCGN) == "eni"
    assert romanize("ကြောင်ဥကျဉ်", BGN_PCGN) == "kyaung-ugyin"
    assert romanize("သဒ္ဒါ", BGN_PCGN) == "thadda"
    assert romanize("အန္တိမဘဝ", BGN_PCGN) == "andimabawa"
    assert romanize("ဥက္ကဌ", BGN_PCGN) == "ukkada"
    assert romanize("ရွှေငန်း", BGN_PCGN) == "shwengan"
    assert romanize("ညီညာ", BGN_PCGN) == "nyinya"
    assert romanize("အင်းကွတ်", BGN_PCGN) == "in-gut"
    assert romanize("ကွန်ရက်", BGN_PCGN) == "kun-yet"
    assert romanize("တိုင်အောင်", BGN_PCGN) == "taing-aung"
    assert romanize("ဟက်ဟက်ပက်ပက်ရယ်", BGN_PCGN) == "het-hetpetpetyè"  # noqa
    assert romanize("ဝသီ", BGN_PCGN) == "wathi"
    assert romanize("ဘေးမဲ့", BGN_PCGN) == "bemè"
    assert romanize("သင်္ဘော", BGN_PCGN) == "thinbaw"
    assert romanize("ဘင်္ဂလားအော်", BGN_PCGN) == "bin-gala-aw"
    assert romanize("စင်္ကာပူ", BGN_PCGN) == "sin-gabu"
