import pytest
from mixer.backend.django import mixer

from django import http
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory
from delete import views

from certifier.models import TrackerCertification, RunReconstruction

pytestmark = pytest.mark.django_db

class TestHardDeleteReferenceView:
    def test_hard_delete_reference_run_post(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))

        assert RunReconstruction.objects.filter(run__run_number=run_number, reconstruction=reco).exists() is True

        arguments={'run_number': run_number, 'reco': reco }

        req = RequestFactory().post(reverse("delete:delete_reference", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        resp = views.hard_delete_reference_run(req, run_number, reco)

        assert 302 == resp.status_code

        assert RunReconstruction.objects.filter(run__run_number=run_number, reconstruction=reco).exists() is False

    def test_hard_delete_reference_run_get(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))

        assert RunReconstruction.objects.filter(run__run_number=run_number, reconstruction=reco).exists() is True

        arguments={'run_number': run_number, 'reco': reco }

        req = RequestFactory().get(reverse("delete:delete_reference", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        resp = views.hard_delete_reference_run(req, run_number, reco)

        assert 200 == resp.status_code

        assert RunReconstruction.objects.filter(run__run_number=run_number, reconstruction=reco).exists() is True

    def test_hard_delete_reference_run_get_does_not_exist(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))

        assert RunReconstruction.objects.filter(run__run_number=run_number, reconstruction=reco).exists() is True

        arguments={'run_number': run_number, 'reco': reco }

        req = RequestFactory().get(reverse("delete:delete_reference", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        resp = views.hard_delete_reference_run(req, run_number, reco)

        with pytest.raises(http.Http404):
            resp = views.hard_delete_reference_run(req, run_number+1, reco)
            assert 200 == resp.status_code and "doesn't exist" in resp.content

        assert RunReconstruction.objects.filter(run__run_number=run_number, reconstruction=reco).exists() is True

class TestHardDeleteView:
    def test_hard_delete_view_post(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))
        trackerCertification = mixer.blend("certifier.TrackerCertification", runreconstruction=runReconstruction)

        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

        arguments={'pk': trackerCertification.pk, 'run_number': run_number, 'reco': reco }

        req = RequestFactory().post(reverse("delete:hard_delete_run", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        resp = views.hard_delete_run_view(req, trackerCertification.pk, run_number, reco)

        assert 302 == resp.status_code

        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is False

    def test_hard_delete_view_get(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))
        trackerCertification = mixer.blend("certifier.TrackerCertification", runreconstruction=runReconstruction)

        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

        arguments={'pk': trackerCertification.pk, 'run_number': run_number, 'reco': reco }

        req = RequestFactory().get(reverse("delete:hard_delete_run", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        resp = views.hard_delete_run_view(req, trackerCertification.pk, run_number, reco)

        assert 200 == resp.status_code

        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

    def test_hard_delete_view_get_does_not_exist(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))
        trackerCertification = mixer.blend("certifier.TrackerCertification", runreconstruction=runReconstruction)

        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

        arguments={'pk': trackerCertification.pk+1, 'run_number': run_number, 'reco': reco }

        req = RequestFactory().get(reverse("delete:hard_delete_run", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        with pytest.raises(http.Http404):
            resp = views.hard_delete_run_view(req, trackerCertification.pk+1, run_number, reco)
            assert 200 == resp.status_code and "doesn't exist" in resp.content

        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True
