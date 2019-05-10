import types

import pytest
from django.test import RequestFactory
from analysis import views
from django.urls import reverse

from analysis.views import *

pytestmark = pytest.mark.django_db

class TestChartData:
    def test_get(self):
        req = RequestFactory().get(reverse("get"))
        chartData=ChartData()
        resp = chartData.get(request=req)

        assert resp.status_code == 200

def test_analyse():
    run_number = 321123
    reco = "express"
    arguments={'run_number': run_number, 'reco': reco }

    req = RequestFactory().get(reverse("analyse", kwargs=arguments))
    resp = views.analyse(req, run_number, reco)

    assert 200 == resp.status_code


