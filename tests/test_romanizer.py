#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from myanmar import language
from myanmar.romanizer import Romanizer, BGN_PCGN

# def test_find_first_position():
#     assert -1 == romanzier.find_first_position("asdf", language.ismyanmar)
#     assert 2 == romanzier.find_first_position(
#         u"as\u1000f", language.ismyconsonant
#     )


def test_myanmar_phonemic_iter():
    def test_myanmar_phonemic_iter_(string, ts=None):
        if not ts:
            ts = "".join(string.split('|'))
        tr = list(language.myanmar_phonemic_iter(ts))
        er = list(e for e in string.split('|'))
        assert tr == er

    test_myanmar_phonemic_iter_(
        "တ|ရား|စီ|ရင်|ရေး|အာ|ဏာ|နှင့်|ဥ|ပ|ဒေ|ပြု|ရေး|အာ|ဏာ|တို့|ကို"
    )
    test_myanmar_phonemic_iter_(
        "မည်|သူ|မ|ဆို| |ကြည့်|ရှု|ပြင်|ဆင်|နိုင်|သော| |" +
        "အ|ခ|မဲ့|လွတ်|လပ်|စွယ်|စုံ|ကျမ်း| |ဖြစ်|ပါ|သည်|။"
    )
    test_myanmar_phonemic_iter_(
        "နာ|နို|တက်|က|နော်|လော်|ဂျီ", ts="နာနိုတက္ကနော်လော်ဂျီ"
    )
    test_myanmar_phonemic_iter_("အို|ရှန်း|နီး|ယား")


def test_bgp_pcgn_romanizer():
    assert Romanizer.romanize(BGN_PCGN, 'ကို') == "ko"
    assert Romanizer.romanize(BGN_PCGN, 'အက') == "aga"
    assert Romanizer.romanize(BGN_PCGN, 'မဒမ') == "madama"
    assert Romanizer.romanize(BGN_PCGN, 'သာငယ်') == 'thangè'
    assert Romanizer.romanize(BGN_PCGN, 'ပြစင်') == 'pyazin'
    assert Romanizer.romanize(BGN_PCGN, 'အကာ') == 'aga'
    assert Romanizer.romanize(BGN_PCGN, 'အိုဘဲ့') == 'obè'
    assert Romanizer.romanize(BGN_PCGN, "အပ်") == "at"
    assert Romanizer.romanize(BGN_PCGN, "မအူ") == "ma-u"
    assert Romanizer.romanize(BGN_PCGN, "သီးပင်အိုင်") == 'thibin-aing'
    assert Romanizer.romanize(BGN_PCGN, "ဩဘာ") == "awba"
    assert Romanizer.romanize(BGN_PCGN, "ဧဏီ") == "eni"
    assert Romanizer.romanize(BGN_PCGN, "ကြောင်ဥကျဉ်") == "kyaung-ugyin"
    assert Romanizer.romanize(BGN_PCGN, "သဒ္ဒါ") == "thadda"
    assert Romanizer.romanize(BGN_PCGN, "အန္တိမဘဝ") == "andimabawa"
    assert Romanizer.romanize(BGN_PCGN, "ဥက္ကဌ") == "ukkada"
    assert Romanizer.romanize(BGN_PCGN, "ရွှေငန်း") == "shwengan"
    assert Romanizer.romanize(BGN_PCGN, "ညီညာ") == "nyinya"
    assert Romanizer.romanize(BGN_PCGN, "အင်းကွတ်") == "in-gut"
    assert Romanizer.romanize(BGN_PCGN, "ကွန်ရက်") == "kun-yet"
    assert Romanizer.romanize(BGN_PCGN, "တိုင်အောင်") == "taing-aung"
    assert Romanizer.romanize(BGN_PCGN, "ဟက်ဟက်ပက်ပက်ရယ်") == "het-hetpetpetyè"
    assert Romanizer.romanize(BGN_PCGN, "ဝသီ") == "wathi"
    assert Romanizer.romanize(BGN_PCGN, "ဘေးမဲ့") == "bemè"
    assert Romanizer.romanize(BGN_PCGN, "သင်္ဘော") == "thinbaw"
    assert Romanizer.romanize(BGN_PCGN, "ဘင်္ဂလားအော်") == "bin-gala-aw"
    assert Romanizer.romanize(BGN_PCGN, "စင်္ကာပူ") == "sin-gabu"
