from decimal import Decimal

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer
from users.models import User
from users.utilities.utilities import *

pytestmark = pytest.mark.django_db

class TestUtilities:
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

    def test_update_user_error(self):
        user = mixer.blend(get_user_model())
        assert user.is_guest

        user=None

        extra_data = {"groups": ["tkdqmdoctor-shiftleaders"]}
        update_user_extradata(user)

        assert True


    def test_update_user(self):
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
