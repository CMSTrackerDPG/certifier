import json
import pytest
from mixer.backend.django import mixer
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from certifier.models import BadReason, TrackerCertification, Dataset, RunReconstruction
from certifier.forms import CertifyForm
from oms.models import OmsRun
from certifier import views
from users.models import User


pytestmark = pytest.mark.django_db


class TestBadReasons:
    def test_bad_reason_get(self):
        """
        Get existing bad reasons
        """
        req = RequestFactory().get(reverse("badreasons"))
        req.user = mixer.blend(User)
        resp = views.badReason(req)
        resp_data = json.loads(resp.content)["bad_reasons"]
        assert len(resp_data) == 0

    def test_bad_reason_post(self):
        """
        Add a new bad reason via POST
        """
        data = {
            "name": "giannhs",
            "description": "ena paidi apo to xwrio den to ksereis",
        }
        req = RequestFactory().post(reverse("badreasons"), data=data)
        req.user = mixer.blend(User)

        resp = views.badReason(req)
        resp_data = json.loads(resp.content)["bad_reasons"]
        assert len(resp_data) == 1
        assert resp_data[0]["name"] == data["name"]
        assert resp_data[0]["description"] == data["description"]

    def test_bad_reason_existing(self):
        """
        Re-add an existing bad reason via POST
        """
        bad_reason = mixer.blend(BadReason)

        req = RequestFactory().post(reverse("badreasons"), data=bad_reason.__dict__)
        req.user = mixer.blend(User)
        resp = views.badReason(req)
        resp_data = json.loads(resp.content)["bad_reasons"]
        assert len(resp_data) == 1
        assert resp_data[0]["id"] == bad_reason.pk
        assert resp_data[0]["name"] == bad_reason.name
        assert resp_data[0]["description"] == bad_reason.description


class TestCertify:
    def test_certify_get(self):
        run_number = 321123
        arguments = {"run_number": run_number}

        req = RequestFactory().get(reverse("certify", kwargs=arguments))

        req.user = mixer.blend(User)

        resp = views.CertifyView.as_view()(req, run_number=run_number)

        assert resp.status_code == 200

    def test_certify_valid(self):
        run_number = 321123
        ref_runReconstruction = mixer.blend(
            RunReconstruction,
            is_reference=True,
            reconstruction=RunReconstruction.EXPRESS,
        )
        bad_reason = mixer.blend(BadReason)
        dataset = mixer.blend(Dataset)
        arguments = {"run_number": run_number}

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
            "external_info_completeness": TrackerCertification.EXTERNAL_INFO_COMPLETE,
        }

        form = CertifyForm(data=data)

        assert {} == form.errors
        assert form.is_valid()

        req = RequestFactory().post(
            reverse("certify", kwargs=arguments), data=form.data
        )
        req.user = mixer.blend(User)
        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)
        resp = views.CertifyView.as_view()(req, run_number=run_number)

        assert resp.status_code, "should redirect to openruns" == 302
        assert TrackerCertification.objects.exists()

    def test_certify_other_users_certification(self):
        """
        Trying to overwrite an existing certification done
        by another user should fail
        """
        user_a = mixer.blend(User)
        user_b = mixer.blend(User)
        run_number = 321123
        run = mixer.blend(OmsRun, run_number=run_number, run_type=OmsRun.COLLISIONS)
        run_reconstruction = mixer.blend(
            RunReconstruction,
            run=run,
            is_reference=False,
            reconstruction=RunReconstruction.EXPRESS,
        )
        ref_run_reconstruction = mixer.blend(RunReconstruction, is_reference=True)
        bad_reason = mixer.blend(BadReason)
        dataset = mixer.blend(Dataset)

        # Certification made by User A
        c = TrackerCertification.objects.create(
            user=user_a,
            runreconstruction=run_reconstruction,
            reference_runreconstruction=ref_run_reconstruction,
            dataset=dataset,
            bad_reason=bad_reason,
            comment="test",
            date="2018-01-01",
            trackermap="exists",
            pixel="good",
            strip="good",
            tracking="good",
        )

        # Create a form using the same data
        form = CertifyForm(instance=c)

        # Create a POST request with this data
        req_url = reverse(
            "certify",
            kwargs={
                "run_number": run_number,
                "reco": run_reconstruction.reconstruction,
            },
        )
        req = RequestFactory().post(req_url, data=form.data)
        # Try to certify as user_b
        req.user = user_b
        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)
        resp = views.CertifyView.as_view()(
            req, run_number=run_number, reco=run_reconstruction.reconstruction
        )
        assert resp.status_code == 400

    def test_recertify_own_certification(self):
        """
        Trying to re-certify an existing certification done
        by the same user shoud redirect to listruns:update
        """
        user_a = mixer.blend(User)
        run_number = 321123
        run = mixer.blend(OmsRun, run_number=run_number, run_type=OmsRun.COLLISIONS)
        run_reconstruction = mixer.blend(
            RunReconstruction,
            run=run,
            is_reference=False,
            reconstruction=RunReconstruction.EXPRESS,
        )
        ref_run_reconstruction = mixer.blend(RunReconstruction, is_reference=True)
        bad_reason = mixer.blend(BadReason)
        dataset = mixer.blend(Dataset)

        # Certification made by User A
        c = TrackerCertification.objects.create(
            user=user_a,
            runreconstruction=run_reconstruction,
            reference_runreconstruction=ref_run_reconstruction,
            dataset=dataset,
            bad_reason=bad_reason,
            comment="test",
            date="2018-01-01",
            trackermap="exists",
            pixel="good",
            strip="good",
            tracking="good",
        )

        # Create a form using the same data
        form = CertifyForm(instance=c)

        # Create a POST request with this data
        req_url = reverse(
            "certify",
            kwargs={
                "run_number": run_number,
                "reco": run_reconstruction.reconstruction,
            },
        )
        req = RequestFactory().post(req_url, data=form.data)

        # Try to certify as same user
        req.user = user_a
        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)
        resp = views.CertifyView.as_view()(
            req, run_number=run_number, reco=run_reconstruction.reconstruction
        )

        assert resp.status_code == 302
        assert resp.url == reverse(
            "listruns:update",
            kwargs={
                "pk": c.pk,
                "run_number": run_number,
                "reco": run_reconstruction.reconstruction,
            },
        )

    def test_certify_invalid_bad_run_number(self):
        run_number = 999999999
        ref_runReconstruction = mixer.blend(RunReconstruction, is_reference=True)
        bad_reason = mixer.blend(BadReason)
        dataset = mixer.blend(Dataset)
        arguments = {"run_number": run_number}

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
            "external_info_completeness": TrackerCertification.EXTERNAL_INFO_COMPLETE,
        }

        form = CertifyForm(data=data)

        assert {} == form.errors
        assert form.is_valid()

        req = RequestFactory().post(
            reverse("certify", kwargs=arguments), data=form.data
        )

        req.user = mixer.blend(User)

        resp = views.CertifyView.as_view()(req, run_number=run_number)

        assert resp.status_code, "should not redirect to success view" == 404
        assert TrackerCertification.objects.exists() is False

    def test_certify_invalid_no_selection(self):
        run_number = 321123
        ref_runReconstruction = mixer.blend(RunReconstruction)
        bad_reason = mixer.blend(BadReason)
        arguments = {"run_number": run_number}

        data = {
            "reference_runreconstruction": ref_runReconstruction.pk,
            "strip": "good",
            "tracking": "good",
            "bad_reason": bad_reason.pk,
            "comment": "test",
            "external_info_completeness": TrackerCertification.EXTERNAL_INFO_INCOMPLETE,
        }

        form = CertifyForm(data=data)

        assert {} != form.errors
        assert form.is_valid() is False

        req = RequestFactory().post(
            reverse("certify", kwargs=arguments), data=form.data
        )
        req.user = mixer.blend(User)
        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)
        resp = views.CertifyView.as_view()(req, run_number=run_number)

        assert resp.status_code, "should not redirect to success view" == 200
        assert TrackerCertification.objects.exists() is False
