#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from myanmar.romanizer import romanize, MLC

def test_romanizer_mlc():
    assert romanize("တက္ကသိုလ်", MLC) == "takkazuilʻ"
    assert romanize("ကမ္ဘာ", MLC) == "kambhā"
    assert romanize("ကော်မီတီ", MLC) == "koʻmītī"
    assert romanize("ပဒေသရာဇာ", MLC) == "padezarājā"
