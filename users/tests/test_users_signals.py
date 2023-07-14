import pytest
from django.db import IntegrityError
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from users.signals import *
from django.test import Client

pytestmark = pytest.mark.django_db


def test_create_user():
    user = mixer.blend(get_user_model())
    user.extra_data = {"hi": "test"}
    assert user


def test_logs():
    """
    Just run them once, nothing really to test here
    """
    log_user_logged_in(None, None, None)
    log_user_logged_out(None, None, None)
    log_user_has_login_failed(None, None, None)
    log_allauth_user_logged_in(None, None)
    log_pre_social_login(None, None)
    log_social_account_added(None, None)
    log_social_account_updated(None, None)
    log_social_account_removed(None, None)


def test_user_automatically_created():
    user = mixer.blend(get_user_model())
    assert user


def test_users_login():
    user = mixer.blend(get_user_model())
    user.set_password("secret")
    user.save()

    assert user.is_guest
    assert not user.is_staff
    assert not user.is_superuser

    client = Client()
    login = client.login(username=user.username, password="secret")

    assert login

    user = get_user_model().objects.get()
    assert user.is_guest
    assert not user.is_staff
    assert not user.is_superuser


def test_update_users_on_save():
    user = mixer.blend(get_user_model())
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_guest
    user.save()
    assert user.is_guest
    extra_data = {"cern_roles": ["admin"]}
    mixer.blend(SocialAccount, user=user, extra_data=extra_data)
    assert user.is_guest
    assert not user.is_staff
    assert not user.is_superuser

    user.save()
    assert not user.is_guest
    assert user.is_staff
    assert user.is_superuser

    user = get_user_model().objects.get()
    assert not user.is_guest
    assert user.is_staff
    assert user.is_superuser
