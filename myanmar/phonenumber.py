# phonenumber.py - phone number validation & normalization module
# coding: utf-8
# The MIT License (MIT)

# Copyright 2016 Melomap (www.melomap.com)
# Copyright 2018 Thura Hlaing (trhura@gmail.com)

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

import re

mobile_code_re = "(09)"
country_code_re = "(\\+?959)"

ooredoo_re = "(?:9(?:7|6|5)\\d{7})$"
mytel_re = "(?:6(?:9|8)\\d{7})$"
telenor_re = "(?:7(?:9|8|7|6)\\d{7})$"
mpt_2_series = "2\\d{6,8}"
mpt_3_series = "3\\d{7,8}"
mpt_4_series = "4\\d{7,8}"
mpt_5_series = "5\\d{6}"
mpt_6_series = "6\\d{6}"
mpt_7_series = "7\\d{7}"
mpt_8_series = "8\\d{6,8}"
mpt_9_series = "9(?:0|1|9)\\d{5,6}"
mpt_re = "(?:{}|{}|{}|{}|{}|{}|{}|{})$".format(
    mpt_2_series, mpt_3_series, mpt_4_series, mpt_5_series, mpt_6_series,
    mpt_7_series, mpt_8_series, mpt_9_series
)

all_operators_re = "({0}|{1}|{2}|{3})".format(
    ooredoo_re, telenor_re, mpt_re, mytel_re
)

mm_phone_re = re.compile(
    "^({0}|{1})?{2}".format(country_code_re, mobile_code_re, all_operators_re)
)


def is_valid_phonenumber(phonenumber):
    """
    Checks whether a given phonenumber is a valid Myanmar number or not.

    >>> is_valid_phonenumber('09420028187')
    True
    >>> is_valid_phonenumber('+959420028187')
    True
    >>> is_valid_phonenumber(9420028187)
    False
    >>> is_valid_phonenumber(94200281870)
    False
    """
    phonenumber = str(phonenumber).strip()
    return mm_phone_re.match(phonenumber) is not None


def normalize_phonenumber(phonenumber):
    """
    Normalize a given phonenumber into ``959xxx`` number format.

    >>> normalize_phonenumber('09420028187')
    959420028187
    >>> normalize_phonenumber('+959420028187')
    959420028187
    >>> normalize_phonenumber('420028187')
    959420028187
    """
    phonenumber = str(phonenumber).strip()
    match = mm_phone_re.match(phonenumber)
    if not match:
        raise RuntimeError(
            "%s is not a valid Myanmar phonenumber." % phonenumber
        )

    phonenumber = match.groups()[3]
    phonenumber = '959' + phonenumber
    return int(phonenumber)
