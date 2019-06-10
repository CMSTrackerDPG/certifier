import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer

from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from summary.views import *

pytestmark = pytest.mark.django_db


def test_view_requires_login():
    req = RequestFactory().get("shiftleader/")
    req.user = AnonymousUser()
    resp = summaryView(req)
    assert resp.status_code == 302

    req.user = mixer.blend(get_user_model())
    resp = summaryView(req)
    assert resp.status_code == 200
