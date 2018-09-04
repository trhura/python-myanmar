import re
from myanmar import phonenumber as mp


def test_with_mobile_code():
    assert re.match(mp.mobile_code_re, "09") is not None
    assert re.match(mp.mobile_code_re, "9") is None
    assert re.match(mp.mobile_code_re, "") is None


def test_with_country_code():
    assert re.match(mp.country_code_re, "+959") is not None
    assert re.match(mp.country_code_re, "959") is not None
    assert re.match(mp.country_code_re, "") is None


def test_telenor():
    assert re.match(mp.telenor_re, "791000481") is not None
    assert re.match(mp.telenor_re, "763619515") is not None
    assert re.match(mp.telenor_re, "991000481") is None


def test_ooredoo():
    assert re.match(mp.ooredoo_re, "962038186") is not None
    assert re.match(mp.ooredoo_re, "791000481") is None
    assert re.match(mp.ooredoo_re, "763619515") is None
    assert re.match(mp.ooredoo_re, "950954940") is not None


def test_mytel():
    assert re.match(mp.mytel_re, "691778993") is not None
    assert re.match(mp.mytel_re, "791000481") is None
    assert re.match(mp.mytel_re, "690000966") is not None


def test_mpt():
    assert re.match(mp.mpt_re, "420090065") is not None
    assert re.match(mp.mpt_re, "5093449") is not None
    assert re.match(mp.mpt_re, "898941022") is not None
    assert re.match(mp.mpt_re, "5093449") is not None
    assert re.match(mp.mpt_re, "763619515") is None


def test_all_operators_re():
    assert re.match(mp.all_operators_re, "420090065") is not None
    assert re.match(mp.all_operators_re, "5093449") is not None
    assert re.match(mp.all_operators_re, "962038186") is not None
    assert re.match(mp.all_operators_re, "791000481") is not None
    assert re.match(mp.all_operators_re, "763619515") is not None


def test_mm_phone_re():
    assert re.match(mp.mm_phone_re, "+959420090065") is not None
    assert re.match(mp.mm_phone_re, "09420090065") is not None
    assert re.match(mp.mm_phone_re, "095093449") is not None
    assert re.match(mp.mm_phone_re, "09962038186") is not None
    assert re.match(mp.mm_phone_re, "959791000481") is not None
    assert re.match(mp.mm_phone_re, "763619515") is not None
    assert re.match(mp.mm_phone_re, "9763619515") is None


def test_is_valid_mm_phone_number():
    assert mp.is_valid_phonenumber("+959420090065") is True
    assert mp.is_valid_phonenumber("959420090065") is True
    assert mp.is_valid_phonenumber("09420090065") is True
    assert mp.is_valid_phonenumber("9420090065") is False
    assert mp.is_valid_phonenumber("420090065") is True

    assert mp.is_valid_phonenumber("+95") is False
    assert mp.is_valid_phonenumber("959") is False
    assert mp.is_valid_phonenumber("+95420090065") is False


def test_normalize_mm_phone_number():
    assert mp.normalize_phonenumber("+959420090065") == 959420090065
    assert mp.normalize_phonenumber("959420090065") == 959420090065
    assert mp.normalize_phonenumber("09420090065") == 959420090065
    assert mp.normalize_phonenumber("420090065") == 959420090065

    assert mp.normalize_phonenumber("+959972991100") == 959972991100
    assert mp.normalize_phonenumber("959972991100") == 959972991100
    assert mp.normalize_phonenumber("09972991100") == 959972991100
    assert mp.normalize_phonenumber("972991100") == 959972991100
