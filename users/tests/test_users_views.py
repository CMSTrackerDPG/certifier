import types

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from mixer.backend.django import mixer

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
