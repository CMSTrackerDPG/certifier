import pytest
from mixer.backend.django import mixer

from django.http import QueryDict
from django.test import RequestFactory
from certifier.models import *
from certifier.forms import *
from oms.models import OmsRun
from certifier import views
from users.models import User
from django.urls import reverse

pytestmark = pytest.mark.django_db

class TestCertify:
    def test_certify_get(self):
        run_number = 321123
        arguments={'run_number': run_number }

        req = RequestFactory().get(reverse("certify", kwargs=arguments))

        req.user = mixer.blend(User)

        resp = views.certify(req, run_number)

        assert 200 == resp.status_code

    def test_certify_valid(self):
        run_number = 321123
        ref_runReconstruction = mixer.blend(RunReconstruction, is_reference=True)
        bad_reason = mixer.blend(BadReason)
        dataset = mixer.blend(Dataset)
        arguments={'run_number': run_number}

        data = {
            "reference_runreconstruction": ref_runReconstruction.pk,
            "dataset": dataset.pk,
            "pixel": "good",
            "strip": "good",
            "tracking": "good",
            "bad_reason": bad_reason.pk,
            "comment": "test",
            "trackermap": "exists",
            "date": "2018-01-01",
        }

        form = CertifyForm(data=data)

        assert {} == form.errors
        assert form.is_valid()

        req = RequestFactory().post(reverse("certify", kwargs=arguments), data=form.data)
        req.user = mixer.blend(User)

        resp = views.certify(req, run_number)

        assert 302 == resp.status_code, "should redirect to success view"
        assert TrackerCertification.objects.exists()

    def test_certify_invalid_bad_run_number(self):
        run_number = 999999999
        ref_runReconstruction = mixer.blend(RunReconstruction, is_reference=True)
        bad_reason = mixer.blend(BadReason)
        dataset = mixer.blend(Dataset)
        arguments={'run_number': run_number}

        data = {
            "reference_runreconstruction": ref_runReconstruction.pk,
            "dataset": dataset.pk,
            "pixel": "good",
            "strip": "good",
            "tracking": "good",
            "bad_reason": bad_reason.pk,
            "comment": "test",
            "trackermap": "exists",
            "date": "2018-01-01",
        }

        form = CertifyForm(data=data)

        assert {} == form.errors
        assert form.is_valid()

        req = RequestFactory().post(reverse("certify", kwargs=arguments), data=form.data)

        req.user = mixer.blend(User)

        resp = views.certify(req, run_number)

        assert 200 == resp.status_code, "should not redirect to success view"
        assert TrackerCertification.objects.exists() == False

    def test_certify_invalid_no_selection(self):
        run_number = 321123
        ref_runReconstruction = mixer.blend(RunReconstruction)
        bad_reason = mixer.blend(BadReason)
        arguments={'run_number': run_number}

        data = {
            "reference_runreconstruction": ref_runReconstruction.pk,
            "strip": "good",
            "tracking": "good",
            "bad_reason": bad_reason.pk,
            "comment": "test",
        }

        form = CertifyForm(data=data)

        assert {} != form.errors
        assert form.is_valid() == False

        req = RequestFactory().post(reverse("certify", kwargs=arguments), data=form.data)
        req.user = mixer.blend(User)

        resp = views.certify(req, run_number)

        assert 200 == resp.status_code, "should not redirect to success view"
        assert TrackerCertification.objects.exists() == False
