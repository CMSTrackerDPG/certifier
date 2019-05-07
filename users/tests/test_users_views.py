import types

import pytest
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.test import Client

from users.views import *

pytestmark = pytest.mark.django_db


def assert_view_requires_no_login(view):
    req = RequestFactory().get("/")
    req.user = AnonymousUser()
    resp = get_view_response(view, req)
    assert resp.status_code == 200 or "login" not in resp.url


def assert_view_requires_login(view):
    req = RequestFactory().get("/")
    req.user = AnonymousUser()

    resp = get_view_response(view, req)
    assert resp.status_code == 302, "should not be anonymous"
    assert "login" in resp.url

    req.user = mixer.blend(get_user_model())
    resp = get_view_response(view, req)
    assert resp.status_code == 200


def assert_view_requires_staff(view):
    with pytest.raises(AssertionError):
        assert_view_requires_login(view)

    req = RequestFactory().get("/")
    req.user = mixer.blend(get_user_model(), is_staff=True)
    resp = get_view_response(view, req)
    assert (
        resp.status_code == 200 or resp.status_code == 302 and "login" not in resp.url
    )


def get_view_response(view, req):
    if isinstance(view, types.FunctionType):
        return view(req)
    return view.as_view()(req)


def test_authentication():
    assert_view_requires_no_login(logout_status)

def test_logout_view_auth():
    req = RequestFactory().get(reverse("users:logout"))
    client=Client()

    req.user = mixer.blend(get_user_model(), username="test", password="test")
    resp = client.post('accounts/login/', username=req.user.username, password=req.user.password , follow=True)

    assert req.user.is_authenticated

    resp = logout(req)


