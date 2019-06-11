import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer

from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from summary.views import *
from summary.utilities.utilities import get_runs_from_request_filters

pytestmark = pytest.mark.django_db


def test_get_runs_from_request_filters():
    alert_errors = []
    alert_infos = []
    alert_filters = []
    run_number1=321123
    run_number2=321126

    user=mixer.blend(get_user_model())
    mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=run_number1)), date="2019-6-10", user=user)
    mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=run_number2)), date="2019-6-16", user=user)

    req = RequestFactory().get("summary/")
    req.GET = req.GET.copy()
    req.GET['date_range_0']="2019-6-10"
    req.GET['date_range_1']="2019-6-16"
    req.GET['runs_0']="321123"
    req.GET['runs_1']="321126"
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert run_number1 == resp[0].runreconstruction.run.run_number
    assert run_number2 == resp[1].runreconstruction.run.run_number

def test_get_runs_from_request_filters_date():
    alert_errors = []
    alert_infos = []
    alert_filters = []
    run_number=321123

    user=mixer.blend(get_user_model())
    mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=run_number)), date="2019-6-10", user=user)

    req = RequestFactory().get("summary/")
    req.GET = req.GET.copy()
    req.GET['date']="2019-6-10"
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert run_number == resp[0].runreconstruction.run.run_number

def test_get_runs_from_request_filters_invalid():
    alert_errors = []
    alert_infos = []
    alert_filters = []
    invalid_date="20199-06-10"
    invalid_run="99das"

    user=mixer.blend(get_user_model())

    req = RequestFactory().get("summary/")
    req.GET = req.GET.copy()
    req.GET['date']=invalid_date
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert invalid_date in alert_errors[0]
    assert not resp

    req = RequestFactory().get("summary/")
    req.GET = req.GET.copy()
    req.GET['date_range_0']=invalid_date
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert invalid_date in alert_errors[1]
    assert not resp

    req = RequestFactory().get("summary/")
    req.GET = req.GET.copy()
    req.GET['date_range_1']=invalid_date
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert invalid_date in alert_errors[2]
    assert not resp

    req = RequestFactory().get("summary/")
    req.GET = req.GET.copy()
    req.GET['runs_0']=invalid_run
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert invalid_run in alert_errors[3]
    assert not resp

    req = RequestFactory().get("summary/")
    req.GET = req.GET.copy()
    req.GET['runs_1']=invalid_run
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert invalid_run in alert_errors[4]
    assert not resp

def test_get_runs_from_request_filters_no_filters():
    alert_errors = []
    alert_infos = []
    alert_filters = []

    user=mixer.blend(get_user_model())

    req = RequestFactory().get("summary/")
    req.user = user

    resp = get_runs_from_request_filters(req, alert_errors, alert_infos, alert_filters)
    assert "No filters applied. Showing every run you have ever certified!" == alert_infos[0]
