import types

import pytest
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from django.urls import reverse
from plot import views
from plot.views import *

pytestmark = pytest.mark.django_db

def test_plot():
    run_number = 321123
    reco = "express"
    arguments={'run_number': run_number, 'reco': reco }

    req = RequestFactory().get(reverse("plot", kwargs=arguments))
    req.user = mixer.blend(get_user_model())
    resp = views.plot(req, run_number, reco)

    assert 200 == resp.status_code
