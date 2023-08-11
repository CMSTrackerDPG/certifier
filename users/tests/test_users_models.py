import pytest
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


class TestUser:
    def test_update_privilege_if_changed(self):
        user = mixer.blend(get_user_model())

        assert user.user_privilege == 0
        user.extra_data = {"cern_roles": ["shifter"]}
        assert user.user_privilege == 0
        user.update_privilege()
        assert user.user_privilege == 10
        user.extra_data.get("cern_roles").append("shiftleader")
        user.update_privilege()
        assert user.user_privilege == 20
        user.extra_data.get("cern_roles").append("expert")
        user.update_privilege()
        assert user.user_privilege == 30
        user.extra_data.get("cern_roles").append("admin")
        user.update_privilege()
        assert user.user_privilege == 50

    def test_upgrade_to_shiftleader(self):
        user = mixer.blend(get_user_model())

        assert user.user_privilege == 0
        user.extra_data = {"cern_roles": ["shiftleader"]}
        user.update_privilege()
        assert user.user_privilege == 20

    def test_downgrade_not_possible(self):
        user = mixer.blend(get_user_model())

        user.extra_data = {"cern_roles": ["admin"]}
        user.update_privilege()
        assert user.user_privilege == 50

        user.extra_data = {"cern_roles": ["shifter"]}
        assert user.user_privilege == 50

        user = mixer.blend(get_user_model())

        user.extra_data = {"cern_roles": ["shiftleader"]}
        user.update_privilege()
        assert user.user_privilege == 20

        user.extra_data = {"cern_roles": ["shifter"]}
        assert user.user_privilege == 20

    def test_properties(self):
        user = mixer.blend(get_user_model())

        assert user.user_privilege == 0
        assert user.is_guest
        assert not user.is_shifter
        assert not user.is_shiftleader
        assert not user.is_expert
        assert not user.is_admin
        assert not user.has_shifter_rights
        assert not user.has_shift_leader_rights
        assert user.is_staff is False
        assert user.is_superuser is False

        user.extra_data = {"cern_roles": ["shifter"]}
        user.update_privilege()
        assert user.user_privilege == 10
        assert not user.is_guest
        assert user.is_shifter
        assert not user.is_shiftleader
        assert not user.is_expert
        assert not user.is_admin
        assert user.has_shifter_rights
        assert not user.has_shift_leader_rights
        assert user.is_staff is False
        assert user.is_superuser is False

        user.extra_data.get("cern_roles").append("shiftleader")
        user.update_privilege()
        assert user.user_privilege == 20
        assert not user.is_guest
        assert not user.is_shifter
        assert user.is_shiftleader
        assert not user.is_expert
        assert not user.is_admin
        assert user.has_shifter_rights
        assert user.has_shift_leader_rights
        assert user.is_staff is True
        assert user.is_superuser is False

        user.extra_data.get("cern_roles").append("expert")
        user.update_privilege()
        assert user.user_privilege == 30
        assert not user.is_guest
        assert not user.is_shifter
        assert not user.is_shiftleader
        assert user.is_expert
        assert not user.is_admin
        assert user.has_shifter_rights
        assert user.has_shift_leader_rights
        assert user.is_staff is True
        assert user.is_superuser is False

        user.extra_data.get("cern_roles").append("admin")
        user.update_privilege()
        assert user.user_privilege == 50
        assert not user.is_guest
        assert not user.is_shifter
        assert not user.is_shiftleader
        assert not user.is_expert
        assert user.is_admin
        assert user.has_shifter_rights
        assert user.has_shift_leader_rights
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_new_user_has_no_rights(self):
        user = mixer.blend(get_user_model())

        assert user.is_staff is False
        assert user.is_superuser is False

        assert user.is_shiftleader is False
        assert user.is_admin is False
        assert user.is_expert is False
        assert user.is_shifter is False
        assert user.is_guest

    def test_update_privilege(self):
        user = mixer.blend(get_user_model())

        assert user.is_guest

        user.extra_data = {"cern_roles": ["shiftleader"]}
        user.update_privilege()

        assert not user.is_guest
        assert user.is_shiftleader
        old_user = get_user_model().objects.get()
        assert old_user.is_guest
        assert not old_user.is_shiftleader

        # User should not be saved unless explicitly wished
        assert old_user.is_staff is False
        assert old_user.is_superuser is False
        assert old_user.is_shiftleader is False
        assert old_user.is_admin is False
        assert old_user.is_expert is False
        assert old_user.is_shifter is False
        assert old_user.is_guest is True

        user.save()
        user = get_user_model().objects.get()
        assert not user.is_guest
        assert user.is_shiftleader

        assert user.is_staff is True
        assert user.is_superuser is False

        assert user.is_shiftleader is True
        assert user.is_admin is False
        assert user.is_expert is False
        assert user.is_shifter is False
        assert user.is_guest is False

    def test_update_privilege_to_shifter(self):
        user = mixer.blend(get_user_model())

        user.extra_data = {"cern_roles": ["shifter"]}
        user.update_privilege()
        user.save()

        user = get_user_model().objects.get()

        assert user.is_staff is False
        assert user.is_superuser is False

        assert user.is_shiftleader is False
        assert user.is_admin is False
        assert user.is_expert is False
        assert user.is_shifter is True
        assert user.is_guest is False

    def test_update_privilege_to_shift_leader(self):
        user = mixer.blend(get_user_model())

        user.extra_data = {"cern_roles": ["shiftleader"]}
        user.update_privilege()
        user.save()

        user = get_user_model().objects.get()

        assert user.is_staff is True
        assert user.is_superuser is False

        assert user.is_shiftleader is True
        assert user.is_admin is False
        assert user.is_expert is False
        assert user.is_shifter is False
        assert user.is_guest is False

    def test_update_privilege_to_expert(self):
        user = mixer.blend(get_user_model())

        user.extra_data = {"cern_roles": ["expert"]}
        user.update_privilege()
        user.save()

        user = get_user_model().objects.get()

        assert user.is_staff is True
        assert user.is_superuser is False

        assert user.is_shiftleader is False
        assert user.is_admin is False
        assert user.is_expert is True
        assert user.is_shifter is False
        assert user.is_guest is False

    def test_update_privilege_to_admin(self):
        user = mixer.blend(get_user_model())

        user.extra_data = {"cern_roles": ["admin"]}
        user.update_privilege()
        user.save()

        user = get_user_model().objects.get()

        assert user.is_staff is True
        assert user.is_superuser is True

        assert user.is_shiftleader is False
        assert user.is_admin is True
        assert user.is_expert is False
        assert user.is_shifter is False
        assert user.is_guest is False

    def test_update_privilege_on_save(self):
        user = mixer.blend(get_user_model())
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_guest

        extra_data = {"cern_roles": ["shiftleader"]}
        account = mixer.blend(SocialAccount, user=user, extra_data=extra_data)
        user.save()
        assert not user.is_guest
        assert user.is_shiftleader
        assert user.is_staff
        assert not user.is_superuser
        account.extra_data = {"cern_roles": ["expert"]}
        account.save()

        user.save()
        assert not user.is_guest
        assert not user.is_shiftleader
        assert user.is_expert
        assert user.is_staff
        assert not user.is_superuser

        updated_user = get_user_model().objects.get()
        assert not updated_user.is_guest
        assert not updated_user.is_shiftleader
        assert updated_user.is_expert
        assert user.is_staff
        assert not user.is_superuser
