import logging

import pytest
from mixer.backend.django import mixer

from credentials import (
    SUPERUSER_USERNAME,
    PASSWORD,
    SHIFTER1_USERNAME,
    SHIFTER2_USERNAME,
    SHIFTLEADER_USERNAME,
    EXPERT_USERNAME,
    ADMIN_USERNAME,
)

pytestmark = pytest.mark.django_db

# Disables Logging when testing
logging.disable(logging.CRITICAL)


@pytest.fixture
def superuser(django_user_model):
    """returns a user with superuser rights"""
    return django_user_model.objects.create_superuser(
        username=SUPERUSER_USERNAME, password=PASSWORD, email=""
    )


@pytest.fixture
def shifter(django_user_model):
    user = django_user_model.objects.create(username=SHIFTER1_USERNAME)
    user.set_password(PASSWORD)
    user.extra_data = {"groups": ["tkdqmdoctor-shifters"]}
    user.update_privilege()
    user.save()
    return user


@pytest.fixture
def second_shifter(django_user_model):
    user = django_user_model.objects.create(username=SHIFTER2_USERNAME)
    user.set_password(PASSWORD)
    user.extra_data = {"groups": ["tkdqmdoctor-shifters"]}
    user.update_privilege()
    user.save()
    return user


@pytest.fixture
def shiftleader(django_user_model):
    user = django_user_model.objects.create(username=SHIFTLEADER_USERNAME)
    user.set_password(PASSWORD)
    user.extra_data = {"groups": ["tkdqmdoctor-shiftleaders"]}
    user.update_privilege()
    user.save()
    return user


@pytest.fixture
def expert(django_user_model):
    user = django_user_model.objects.create(username=EXPERT_USERNAME)
    user.set_password(PASSWORD)
    user.extra_data = {"groups": ["tkdqmdoctor-experts"]}
    user.update_privilege()
    user.save()
    return user


@pytest.fixture
def admin(django_user_model):
    user = django_user_model.objects.create(username=ADMIN_USERNAME)
    user.set_password(PASSWORD)
    user.extra_data = {"groups": ["tkdqmdoctor-admins"]}
    user.update_privilege()
    user.save()
    return user


