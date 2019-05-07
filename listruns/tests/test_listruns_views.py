import pytest
from mixer.backend.django import mixer

from django.http import QueryDict
from django.test import RequestFactory
from certifier.models import *
from certifier.forms import *
from oms.models import OmsRun
from listruns import views
from users.models import User
from django.urls import reverse

pytestmark = pytest.mark.django_db

class TestListRuns:
    def test_certify(self):
        req = RequestFactory().post(reverse("listruns:list"))
        resp = views.listruns(req)
        assert 302 == resp.status_code

    def test_certify_button_redirect(self):
        req = RequestFactory().post(reverse("listruns:list"))
        req.GET = req.GET.copy()
        req.GET['run_number'] = 321123
        req.GET['reco'] = "express"
        resp = views.listruns(req)
        assert 302 == resp.status_code


