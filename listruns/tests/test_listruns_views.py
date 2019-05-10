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
from listruns.utilities.utilities import get_today_filter_parameter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

pytestmark = pytest.mark.django_db

def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.
    """

    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

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

    def test_listruns_authenticated(self):
        req = RequestFactory().post("/list/%s" % get_today_filter_parameter())
        req.user=mixer.blend(get_user_model())
        resp = views.listruns(req)
        assert 200 == resp.status_code

    def test_listrunsi_not_authenticated(self):
        req = RequestFactory().post("/list/%s" % get_today_filter_parameter())
        req.user=AnonymousUser()
        resp = views.listruns(req)
        assert 200 == resp.status_code

    def test_listrunsi_not_authenticated_filters(self):
        req = RequestFactory().post("list/?options=on&date_range_min=1990-12-07&date_range_max=2019-12-07")
        req.user=AnonymousUser()
        resp = views.listruns(req)
        assert 200 == resp.status_code

    def test_update_logged(self):
        trackerCertification = mixer.blend(TrackerCertification)
        arguments={'pk': trackerCertification.pk, 'run_number': trackerCertification.runreconstruction.run.run_number, 'reco': trackerCertification.runreconstruction.reconstruction }

        req = RequestFactory().get(reverse("listruns:update", kwargs=arguments))

        req.user = mixer.blend(get_user_model())

        resp=views.UpdateRun.as_view()(req, pk=trackerCertification.pk)

        assert 302 == resp.status_code

    def test_update_not_logged(self):
        trackerCertification = mixer.blend(TrackerCertification)
        arguments={'pk': trackerCertification.pk, 'run_number': trackerCertification.runreconstruction.run.run_number, 'reco': trackerCertification.runreconstruction.reconstruction }

        req = RequestFactory().get(reverse("listruns:update", kwargs=arguments))

        req.user = AnonymousUser()

        resp=views.UpdateRun.as_view()(req, pk=trackerCertification.pk)

        assert 302 == resp.status_code

    def test_update_not_logged_dispatch(self):
        runReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        referenceRunReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        trackerCertification = mixer.blend(TrackerCertification, reference_runreconstruction=referenceRunReconstruction, runreconstruction=runReconstruction)

        arguments={'pk': trackerCertification.pk, 'run_number': trackerCertification.runreconstruction.run.run_number, 'reco': trackerCertification.runreconstruction.reconstruction }

        req = RequestFactory().get(reverse("listruns:update", kwargs=arguments))

        user = mixer.blend(get_user_model())
        user.extra_data = {"groups": ["tkdqmdoctor-shiftleaders"]}
        user.update_privilege()
        user.save()

        req.user=user

        view = setup_view(views.UpdateRun(), req, pk=trackerCertification.pk, run_number=arguments['run_number'], reco=arguments['reco'])
        resp = view.dispatch(req)

        assert 200 == resp.status_code

    def test_update_get_success_url(self):
        runReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        referenceRunReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        trackerCertification = mixer.blend(TrackerCertification, reference_runreconstruction=referenceRunReconstruction, runreconstruction=runReconstruction)

        arguments={'pk': trackerCertification.pk, 'run_number': trackerCertification.runreconstruction.run.run_number, 'reco': trackerCertification.runreconstruction.reconstruction }

        req = RequestFactory().get(reverse("listruns:update", kwargs=arguments))

        user = mixer.blend(get_user_model())
        user.extra_data = {"groups": ["tkdqmdoctor-shiftleaders"]}
        user.update_privilege()
        user.save()

        req.user=user

        view = setup_view(views.UpdateRun(), req, pk=trackerCertification.pk, run_number=arguments['run_number'], reco=arguments['reco'])
        resp = view.get_success_url()

        assert "/" == resp

    def test_update_same_user_or_shiftleader_true(self):
        runReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        referenceRunReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        trackerCertification = mixer.blend(TrackerCertification, reference_runreconstruction=referenceRunReconstruction, runreconstruction=runReconstruction)

        arguments={'pk': trackerCertification.pk, 'run_number': trackerCertification.runreconstruction.run.run_number, 'reco': trackerCertification.runreconstruction.reconstruction }

        req = RequestFactory().get(reverse("listruns:update", kwargs=arguments))

        user = mixer.blend(get_user_model())
        user.extra_data = {"groups": ["tkdqmdoctor-shiftleaders"]}
        user.update_privilege()
        user.save()

        req.user=user

        view = setup_view(views.UpdateRun(), req, pk=trackerCertification.pk, run_number=arguments['run_number'], reco=arguments['reco'])
        resp = view.same_user_or_shiftleader(req.user)

        assert True == resp

    def test_update_same_user_or_shiftleader_false(self):
        runReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        referenceRunReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun))
        trackerCertification = mixer.blend(TrackerCertification, reference_runreconstruction=referenceRunReconstruction, runreconstruction=runReconstruction)

        arguments={'pk': trackerCertification.pk, 'run_number': trackerCertification.runreconstruction.run.run_number, 'reco': trackerCertification.runreconstruction.reconstruction }

        req = RequestFactory().get(reverse("listruns:update", kwargs=arguments))

        user = mixer.blend(get_user_model())
        user_aux = mixer.blend(get_user_model())
        user.extra_data = {"groups": ["tkdqmdoctor-shiftleaders"]}
        user.update_privilege()
        user.save()

        req.user=user

        view = setup_view(views.UpdateRun(), req, pk=trackerCertification.pk, run_number=arguments['run_number'], reco=arguments['reco'])
        resp = view.same_user_or_shiftleader(user_aux)

        assert False == resp
