import re
from myanmar import phonenumber as mp


def test_with_mobile_code():
    assert re.match(mp.mobile_code, "09") is not None
    assert re.match(mp.mobile_code, "9") is None
    assert re.match(mp.mobile_code, "") is None


def test_with_country_code():
    assert re.match(mp.country_code, "+959") is not None
    assert re.match(mp.country_code, "959") is not None
    assert re.match(mp.country_code, "") is None


def test_telenor():
    numbers = [
        "791000481",
        "781000481",
        "771000001",
        "763619515",
        "750000001",
        "759000001"
    ]
    for each in numbers:
        assert re.match(mp.telenor, each) is not None
    assert re.match(mp.telenor, "991000481") is None


def test_ooredoo():
    assert re.match(mp.ooredoo, "988833358") is not None
    assert re.match(mp.ooredoo, "962038186") is not None
    assert re.match(mp.ooredoo, "791000481") is None
    assert re.match(mp.ooredoo, "763619515") is None
    assert re.match(mp.ooredoo, "950954940") is not None


def test_mytel():
    assert re.match(mp.mytel, "691778993") is not None
    assert re.match(mp.mytel, "791000481") is None
    assert re.match(mp.mytel, "690000966") is not None
    assert re.match(mp.mytel, "683004063") is not None
    assert re.match(mp.mytel, "783004063") is None
    assert re.match(mp.mytel, "672623657") is not None


def test_mpt():
    assert re.match(mp.mpt, "420090065") is not None
    assert re.match(mp.mpt, "5093449") is not None
    assert re.match(mp.mpt, "898941022") is not None
    assert re.match(mp.mpt, "5093449") is not None
    assert re.match(mp.mpt, "763619515") is None


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


def test_check_operator():
    assert mp.get_phone_operator("+959262624625") is mp.Operator.Mpt
    assert mp.get_phone_operator("09970000234") is mp.Operator.Ooredoo
    assert mp.get_phone_operator("09770563818") is mp.Operator.Telenor
    assert mp.get_phone_operator("691877022") is mp.Operator.Mytel
    assert mp.get_phone_operator("123456789") is mp.Operator.Unknown


def test_landline_operator():
    assert mp.get_landline_operator('+95674601234') is "MyanmarAPN"
    assert mp.get_landline_operator('9514244321') is "FortuneInternational"
