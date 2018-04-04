#!/usr/bin/env python

# Copyright 2016 Melomap (www.melomap.com)
# Copyright 2018 Thura Hlaing (trhura@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re

mobile_code_re = "(0?9)"
country_code_re = "(\\+?95)"

ooredoo_re = "(?:9(?:7|6|5)\\d{7})$"
telenor_re = "(?:7(?:9|8|7|6)\\d{7})$"
mpt_2_series = "2\\d{6,8}"
mpt_3_series = "3\\d{7,8}"
mpt_4_series = "4\\d{7,8}"
mpt_5_series = "5\\d{6}"
mpt_6_series = "6\\d{6}"
mpt_7_series = "7\\d{7}"
mpt_8_series = "8\\d{6}"
mpt_9_series = "9(?:0|1|9)\\d{5,6}"
mpt_re = "(?:{}|{}|{}|{}|{}|{}|{}|{})$".format(
    mpt_2_series, mpt_3_series, mpt_4_series, mpt_5_series, mpt_6_series,
    mpt_7_series, mpt_8_series, mpt_9_series
)

all_operators_re = "({0}|{1}|{2})".format(ooredoo_re, telenor_re, mpt_re)

mm_phone_re = re.compile(
    "^({0}?{1})?{2}".format(country_code_re, mobile_code_re, all_operators_re)
)


def is_valid_mm_phonenumber(phonenumber):
    phonenumber = str(phonenumber).strip()
    return mm_phone_re.match(phonenumber) is not None


def normalize_mm_phonenumber(phonenumber):
    phonenumber = str(phonenumber).strip()
    match = mm_phone_re.match(phonenumber)
    if not match:
        raise RuntimeError(
            "%s is not a valid Myanmar phonenumber." % phonenumber
        )

    phonenumber = match.groups()[3]
    phonenumber = '959' + phonenumber
    return int(phonenumber)
