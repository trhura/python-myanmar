from myanmar import nrc as nm


def test_is_valid_nrc():
    assert nm.is_valid_nrc('9/pmn(n)1234560') is RuntimeError
    assert nm.is_valid_nrc('15/pmn(n)123456') is False
    assert nm.is_valid_nrc('5/pmn(n)123456') is False
    assert nm.is_valid_nrc('9/pmn(t)123456') is False
    assert nm.is_valid_nrc('1/ygn(n)123456') is False

    assert nm.is_valid_nrc('9/pmn(n)123456') is True
    assert nm.is_valid_nrc('9/pmn(p)123456') is True
    assert nm.is_valid_nrc('9/pmn(e)123456') is True
    assert nm.is_valid_nrc('9/pmn(naing)123456') is True
    assert nm.is_valid_nrc('9/p m n(naing) 123456') is True


def test_normalize_nrc():
    assert nm.normalize_nrc('9/pmn(n)123456') == '9 pamana n 123456'
    assert nm.normalize_nrc('9/pamana(p)123456') == '9 pamana p 123456'
    assert nm.normalize_nrc('9/pmn(naing)123456') == '9 pamana n 123456'
