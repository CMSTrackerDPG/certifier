import pytest
import os
from django.test import RequestFactory
from mixer.backend.django import mixer

from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from shiftleader.views import *
from users.models import User
from utilities.utilities import create_runs

pytestmark = pytest.mark.django_db


def test_view_requires_login():
    req = RequestFactory().get("shiftleader/")
    req.user = AnonymousUser()
    resp = shiftleader_view(req)
    assert resp.status_code == 302

    req.user = mixer.blend(get_user_model())
    resp = shiftleader_view(req)
    assert resp.status_code == 302

    req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)
    resp = shiftleader_view(req)
    # Navigating to shiftleader URL adds the GET date parameters
    assert resp.status_code == 302 and "date" in resp.url


def test_view_with_request_arguments():
    req = RequestFactory().get(reverse("shiftleader:shiftleader"))
    req.GET = req.GET.copy()
    req.GET["date__gte"] = "2019-6-10"
    req.GET["date__lte"] = "2019-6-16"

    # Shiftleaders can access it
    req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)
    resp = shiftleader_view(req)
    assert resp.status_code == 200

    # Normal users should be redirected.. right?
    req.user = mixer.blend(get_user_model())
    resp = shiftleader_view(req)
    assert resp.status_code == 302


@pytest.mark.skipif(
    "GITHUB_ACTIONS" in os.environ,
    reason="skipped due to GitHub actions not being able to run it",
)
def test_view_compare_with_run_registry():
    create_runs(3, 1, "collisions", "express", date="2018-05-14")
    req = RequestFactory().get("shiftleader/")
    req.GET = req.GET.copy()
    req.GET["date__gte"] = "2018-5-13"
    req.GET["date__lte"] = "2018-5-16"
    req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)
    resp = shiftleader_view(req)
    assert resp.status_code == 200
