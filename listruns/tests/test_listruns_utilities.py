from decimal import Decimal

import pytest
from users.models import User
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer

from shiftleader.utilities.utilities import get_this_week_filter_parameter
from listruns.utilities.utilities import *
from listruns.utilities.manip import *
from listruns.utilities.luminosity import *
from certifier.models import *

pytestmark = pytest.mark.django_db

def test_manip():
    result = strip_trailing_zeros("1.000")
    assert '1' == result
    result = strip_trailing_zeros("1.12345000")
    assert '1.12345' == result
    result = strip_trailing_zeros("34")
    assert '34' == result
    result = strip_trailing_zeros(Decimal("1.120"))
    assert '1.12' == result
    result = strip_trailing_zeros("0.34")
    assert '0.34' == result

def test_luminosity():
    result = format_integrated_luminosity(Decimal("0.000000266922"))
    assert '0.267 µb⁻¹' ==  result
    result = format_integrated_luminosity(Decimal("1.12345678901234567890"))
    assert '1.123 pb⁻¹' ==  result

def test_is_valid_date():
    assert True is is_valid_date("1999-01-01")
    assert True is is_valid_date("2000-12-31")
    assert True is is_valid_date("2018-02-28")
    assert True is is_valid_date("2018-02-28")
    assert False is is_valid_date("2018-02-29")
    assert True is is_valid_date("2020-02-29")
    assert False is is_valid_date("2020-02-30")
    assert True is is_valid_date("5362-02-13")

def test_get_date_string():
    assert get_date_string("1900", "01", "01") == "1900-01-01"
    assert get_date_string("2099", "12", "31") == "2099-12-31"
    assert get_date_string("2999", "3", "7") == "2999-03-07"
    assert get_date_string("2018", "5", "31") == "2018-05-31"
    # assert get_date_string("2018", "03", "29") == ""
    assert get_date_string("2018", "03", "28") == "2018-03-28"
    assert get_date_string("2018", "", "28") == ""
    # assert get_date_string("a", "03", "28") == ""
    # assert get_date_string("2018", "bcd", "29") == ""
    # assert get_date_string("2018", "03", "!") == ""

def test_is_valid_id():
    run = mixer.blend("certifier.RunReconstruction")
    assert True is is_valid_id(run.pk, RunReconstruction)
    assert False is is_valid_id(run.pk + 1, RunReconstruction)
    assert False is is_valid_id("3", RunReconstruction)
    assert False is is_valid_id("a", RunReconstruction)
    assert True is is_valid_id(str(run.pk), RunReconstruction)

def test_get_this_week_filter_parameter():
    # TODO better test
    param = get_this_week_filter_parameter()
    assert param.startswith("?date__gte")
    assert "date__lte" in param

def test_request_contains_filter_parameter():
    req = RequestFactory().get("/")
    assert False is request_contains_filter_parameter(req)
    user = mixer.blend(User)
    req.GET = req.GET.copy()
    req.GET["userid"] = user.id
    assert True is request_contains_filter_parameter(req)
    req = RequestFactory().get("/")
    req.GET = req.GET.copy()
    assert False is request_contains_filter_parameter(req)
    req.GET["date_year"] = "2017"
    assert True is request_contains_filter_parameter(req)

def test_decimal_or_none():
    assert decimal_or_none("2.1") == Decimal("2.1")
    assert decimal_or_none("2.1.0") is None
    assert decimal_or_none(2.0) == Decimal("2")
    assert decimal_or_none(None) is None
    assert decimal_or_none(13) == Decimal("13")
    assert decimal_or_none(-1) == Decimal("-1")
    assert decimal_or_none(".314") == Decimal("0.314")
    assert decimal_or_none(0.5) == Decimal(".5")

def test_integer_or_none():
    assert integer_or_none("13") == 13
    assert integer_or_none("13.7") == 13
    assert integer_or_none("13.7.3") is None
    assert integer_or_none("abc") is None
    assert integer_or_none("0") == 0
    assert integer_or_none(0) == 0
    assert integer_or_none("-1.2") == -1
    assert integer_or_none("-31.7") == -31
    assert integer_or_none(".3") == 0

def test_boolean_or_none():
    """
    Returns the value casted as boolean or None if casting failed.

    "true" -> True
    "tRuE" -> True
    "false" -> False
    "" -> None
    "abc" -> None
    0 -> False
    "1" -> True
    1 -> True
    2 -> None
    """
    assert boolean_or_none("1") is True
    assert boolean_or_none("true") is True
    assert boolean_or_none("tRuE") is True
    assert boolean_or_none("false") is False
    assert boolean_or_none("") is None
    assert boolean_or_none(None) is None
    assert boolean_or_none(True) is True
    assert boolean_or_none(False) is False
    assert boolean_or_none("0") is False
    assert boolean_or_none(1) is True
    assert boolean_or_none(0) is False
    assert boolean_or_none(-1) is None
    assert boolean_or_none(2) is None
    assert boolean_or_none("abc") is None
