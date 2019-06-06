import pytest
from mixer.backend.django import mixer

from django import http
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory
from restore import views

from certifier.models import TrackerCertification

pytestmark = pytest.mark.django_db

class TestRestoreView:
    def test_restore_view_post(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))
        trackerCertification = mixer.blend("certifier.TrackerCertification", runreconstruction=runReconstruction)

        TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).delete()

        assert TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number).exists() is False
        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

        arguments={'pk': trackerCertification.pk, 'run_number': run_number, 'reco': reco }

        req = RequestFactory().post(reverse("restore:restore_run", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        resp = views.restore_run_view(req, trackerCertification.pk, run_number, reco)

        assert 302 == resp.status_code

        assert TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number).exists() is True

    def test_hard_delete_view_get(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))
        trackerCertification = mixer.blend("certifier.TrackerCertification", runreconstruction=runReconstruction)

        TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).delete()

        assert TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number).exists() is False
        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

        arguments={'pk': trackerCertification.pk, 'run_number': run_number, 'reco': reco }

        req = RequestFactory().get(reverse("restore:restore_run", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        resp = views.restore_run_view(req, trackerCertification.pk, run_number, reco)

        assert 200 == resp.status_code

        assert TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number).exists() is False
        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

    def test_hard_delete_view_get_does_not_exist(self):
        run_number = 321123
        reco = "express"

        runReconstruction = mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=run_number))
        trackerCertification = mixer.blend("certifier.TrackerCertification", runreconstruction=runReconstruction)

        TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).delete()

        assert TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number).exists() is False
        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True

        arguments={'pk': trackerCertification.pk+1, 'run_number': run_number, 'reco': reco }

        req = RequestFactory().get(reverse("restore:restore_run", kwargs=arguments))
        req.user = mixer.blend(get_user_model())

        with pytest.raises(http.Http404):
            resp = views.restore_run_view(req, trackerCertification.pk+1, run_number, reco)
            assert 200 == resp.status_code and "doesn't exist" in resp.content

        assert TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number).exists() is False
        assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=run_number).exists() is True
