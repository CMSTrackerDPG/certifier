import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer

from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from shiftleader.views import *

pytestmark = pytest.mark.django_db


def test_view_requires_login():
    req = RequestFactory().get("shiftleader/")
    req.user = AnonymousUser()
    resp = shiftleader_view(req)
    assert resp.status_code == 302

    req.user = mixer.blend(get_user_model())
    resp = shiftleader_view(req)
    assert resp.status_code == 302 and "date" in resp.url

def test_view_with_request_arguments():
    req = RequestFactory().get(reverse("shiftleader:shiftleader"))
    req.GET = req.GET.copy()
    req.GET['date__gte']="2019-6-10"
    req.GET['date__lte']="2019-6-16"
    req.user = mixer.blend(get_user_model())
    resp = shiftleader_view(req)
    assert resp.status_code == 200


