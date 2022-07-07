import pytest
import json
from mixer.backend.django import mixer

from django.http import QueryDict
from django.test import RequestFactory
from certifier.models import *
from oms.models import OmsRun
from oms.exceptions import OmsApiRunNumberNotFound
from addrefrun import views
from users.models import User
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage

pytestmark = pytest.mark.django_db


class TestAddReference:
    def test_addreference_get(self):
        req = RequestFactory().get(reverse("addrefrun:addrefrun"))

        req.user = AnonymousUser()

        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)

        resp = views.addreference(req)

        assert 302 == resp.status_code

    def test_addreference_get_login(self):
        req = RequestFactory().get(reverse("addrefrun:addrefrun"))

        req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)

        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)

        resp = views.addreference(req)

        assert 200 == resp.status_code

    def test_addreference_valid(self):
        run_number = 321123
        reco = "express"
        arguments = {"run_number": run_number, "reco": reco}

        req = RequestFactory().get(reverse("addrefrun:addrefrun"))
        req.GET = req.GET.copy()
        req.GET["run_number"] = run_number
        req.GET["reco"] = reco
        req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)

        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)

        resp = views.addreference(req)

        assert 200 == resp.status_code
        assert RunReconstruction.objects.get(
            run__run_number=run_number, reconstruction=reco
        )

        # Non-shiftleaders are redirected
        req.user = AnonymousUser()
        resp = views.addreference(req)
        assert 302 == resp.status_code

    def test_addreference_invalid(self):
        run_number = 9999999
        reco = "express"
        arguments = {"run_number": run_number, "reco": reco}

        req = RequestFactory().get(reverse("addrefrun:addrefrun"))
        req.GET = req.GET.copy()
        req.GET["run_number"] = run_number
        req.GET["reco"] = reco
        req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)

        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)

        with pytest.raises(OmsApiRunNumberNotFound):
            resp = views.addreference(req)

        assert not RunReconstruction.objects.exists()

        # Non-shiftleaders are redirected
        req.user = AnonymousUser()

        resp = views.addreference(req)
        assert resp.status_code == 302

    def test_addreference_already_exists(self):
        run_number = 321123
        reco = "express"
        mixer.blend(
            RunReconstruction,
            reconstruction=reco,
            run=mixer.blend(OmsRun, run_number=run_number),
        )
        assert RunReconstruction.objects.exists()

        arguments = {"run_number": run_number, "reco": reco}

        req = RequestFactory().get(reverse("addrefrun:addrefrun"))
        req.GET = req.GET.copy()
        req.GET["run_number"] = run_number
        req.GET["reco"] = reco
        req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)

        setattr(req, "session", "session")
        messages = FallbackStorage(req)
        setattr(req, "_messages", messages)

        resp = views.addreference(req)

        assert 200 == resp.status_code
        assert RunReconstruction.objects.exists()
        assert RunReconstruction.objects.all().count() == 1


class TestUpdateReferenceReconstructionRunsInfo:
    def test_update_refruns_info(self):
        """
        Create a reference runreconstruction and a run
        corresponding to it, and try the update_refruns_info endpoint
        """
        run_number = 321123
        mixer.blend(
            RunReconstruction,
            reconstruction=RunReconstruction.EXPRESS,
            run=mixer.blend(OmsRun, run_number=run_number),
            is_reference=True,
        )
        req = RequestFactory().get(reverse("addrefrun:update_refruns_info"))
        req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)
        resp = views.update_refruns_info(req)

        # Response is a JSON with a "success" key
        data = json.loads(resp.content.decode("utf-8"))
        assert data["success"] is True
