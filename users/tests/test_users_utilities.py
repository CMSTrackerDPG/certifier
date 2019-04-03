from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer

from users.utilities.utilities import *

pytestmark = pytest.mark.django_db


class TestUtilities:
    def test_is_valid_date(self):
        assert True is is_valid_date("1999-01-01")
        assert True is is_valid_date("2000-12-31")
        assert True is is_valid_date("2018-02-28")
        assert True is is_valid_date("2018-02-28")
        assert False is is_valid_date("2018-02-29")
        assert True is is_valid_date("2020-02-29")
        assert False is is_valid_date("2020-02-30")
        assert True is is_valid_date("5362-02-13")

    def test_get_date_string(self):
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

    def test_to_date(self):
        d = to_date("2018-02-28")
        assert d == datetime.date(2018, 2, 28)
        assert to_date(datetime.date(2019, 12, 29)) == datetime.date(2019, 12, 29)
        assert to_date(datetime.datetime(2017, 1, 2, 3, 4, 5)) == datetime.date(
            2017, 1, 2
        )

        with pytest.raises(ValueError):
            to_date("2018-02-29")

    def test_to_weekdayname(self):
        assert to_weekdayname(to_date("2018-06-12")) == "Tuesday"

    def test_get_full_name(self):
        user1 = mixer.blend(
            get_user_model(), username="abcdef1", first_name="Hans", last_name="Skywalker"
        )
        user2 = mixer.blend(
            get_user_model(), username="abcdef2", first_name="", last_name="Skywalker"
        )
        user3 = mixer.blend(get_user_model(), username="abcdef3", first_name="Hans", last_name="")
        user4 = mixer.blend(get_user_model(), username="abc def4", first_name="", last_name="")

        assert get_full_name(user1) == "Hans Skywalker (abcdef1)"
        assert get_full_name(user2) == "Skywalker (abcdef2)"
        assert get_full_name(user3) == "Hans (abcdef3)"
        assert get_full_name(user4) == "abc def4"

    def test_get_this_week_filter_parameter(self):
        # TODO better test
        param = get_this_week_filter_parameter()
        assert param.startswith("?date__gte")
        assert "date__lte" in param

    def test_request_contains_filter_parameter(self):
        req = RequestFactory().get("/")
        assert False is request_contains_filter_parameter(req)
        user = mixer.blend(get_user_model())
        req.GET = req.GET.copy()
        req.GET["userid"] = user.id
        assert True is request_contains_filter_parameter(req)
        req = RequestFactory().get("/")
        req.GET = req.GET.copy()
        assert False is request_contains_filter_parameter(req)
        req.GET["date_year"] = "2017"
        assert True is request_contains_filter_parameter(req)

    def test_extract_egroups(self):
        egroups = extract_egroups({})
        assert egroups is None
        egroups = extract_egroups({"test": ["something", "wrong"]})
        assert egroups is None
        egroups = extract_egroups(
            {"unrelated": None, "groups": ["correct", "groups"], "name": "Frank"}
        )
        assert ["correct", "groups"] == egroups

    def test_get_highest_privilege_from_egroup_list(self):
        egroups = ["useless"]
        criteria_dict = {
            10: ["useful", "slightly useful"],
            20: ["more useful"],
            30: ["very useful"],
            50: ["most useful"],
        }

        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert 0 == privilege

        egroups.append("slightly useful")
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert 10 == privilege

        egroups.append("more useful")
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert 20 == privilege

        egroups.append("useful")
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert 20 == privilege

        egroups.append("most useful")
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert 50 == privilege

        egroups.append("very useful")
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert 50 == privilege

    def test_get_highest_privilege_from_egroup_list_real_data(self):
        GUEST = 0
        SHIFTER = 10
        SHIFTLEADER = 20
        EXPERT = 30
        ADMIN = 50

        criteria_dict = {
            SHIFTER: ["tkdqmdoctor-shifters"],
            SHIFTLEADER: [
                "cms-tracker-offline-shiftleader",
                "cms-tracker-offline-shiftleaders",
                "tkdqmdoctor-shiftleaders",
            ],
            EXPERT: ["tkdqmdoctor-experts"],
            ADMIN: ["tkdqmdoctor-admins"],
        }

        egroups = []
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert GUEST == privilege

        egroups = ["tkdqmdoctor-shifters"]
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert SHIFTER == privilege

        egroups = ["cms-tracker-offline-shiftleaders"]
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert SHIFTLEADER == privilege

        egroups = [
            "cms-tracker-offline-shiftleaders",
            "tkdqmdoctor-experts",
            "tkdqmdoctor-shifters",
        ]
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert EXPERT == privilege

        egroups = [
            "cms-tracker-offline-shiftleaders",
            "tkdqmdoctor-admins",
            "tkdqmdoctor-experts",
            "tkdqmdoctor-shifters",
        ]
        privilege = get_highest_privilege_from_egroup_list(egroups, criteria_dict)
        assert ADMIN == privilege

    def test_get_or_create_group(self):
        assert not Group.objects.exists()
        group = get_or_create_group("Shift leaders")

        assert Group.objects.exists()
        assert group == Group.objects.get()
        assert group.name == "Shift leaders"

        group = get_or_create_group("Shift leaders")
        assert group == Group.objects.get()

    def test_update_userprofile(self):
        user = mixer.blend(get_user_model())
        assert user.is_guest

        extra_data = {"groups": ["tkdqmdoctor-shiftleaders"]}
        account = mixer.blend(SocialAccount, user=user, extra_data=extra_data)
        update_user_extradata(user)
        assert not user.is_guest
        assert user.is_shiftleader
        account.extra_data = {"groups": ["tkdqmdoctor-experts"]}
        account.save()

        update_user_extradata(user)
        assert not user.is_guest
        assert not user.is_shiftleader
        assert user.is_expert

        unsaved_user = get_user_model().objects.get()
        assert unsaved_user.is_guest
        assert not unsaved_user.is_shiftleader
        assert not unsaved_user.is_expert

        user.save()
        updated_user = get_user_model().objects.get()
        assert not updated_user.is_guest
        assert not updated_user.is_shiftleader
        assert updated_user.is_expert

    def test_decimal_or_none(self):
        assert decimal_or_none("2.1") == Decimal("2.1")
        assert decimal_or_none("2.1.0") is None
        assert decimal_or_none(2.0) == Decimal("2")
        assert decimal_or_none(None) is None
        assert decimal_or_none(13) == Decimal("13")
        assert decimal_or_none(-1) == Decimal("-1")
        assert decimal_or_none(".314") == Decimal("0.314")
        assert decimal_or_none(0.5) == Decimal(".5")

    def test_integer_or_none(self):
        assert integer_or_none("13") == 13
        assert integer_or_none("13.7") == 13
        assert integer_or_none("13.7.3") is None
        assert integer_or_none("abc") is None
        assert integer_or_none("0") == 0
        assert integer_or_none(0) == 0
        assert integer_or_none("-1.2") == -1
        assert integer_or_none("-31.7") == -31
        assert integer_or_none(".3") == 0

    def test_boolean_or_none(self):
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
