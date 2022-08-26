import pytest
import json
from django.test import RequestFactory
from mixer.backend.django import mixer

from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from users.models import User
from summary.views import SummaryView
from summary.forms import SummaryExtraInfoForm
from oms.models import OmsRun
from certifier.models import TrackerCertification

pytestmark = pytest.mark.django_db


def test_view_requires_shifter_rights():
    #
    req = RequestFactory().get(reverse("summary:summary"))
    req.user = AnonymousUser()
    resp = SummaryView.as_view()(req)
    assert resp.status_code == 302

    req.user = mixer.blend(User, user_privilege=User.SHIFTER)

    resp = SummaryView.as_view()(req)
    assert resp.status_code == 200


def test_get_success():

    user = mixer.blend(User, user_privilege=User.SHIFTER)
    certs = [
        mixer.blend(
            TrackerCertification, runreconstruction__run__run_number=355555, user=user
        ),
        mixer.blend(
            TrackerCertification, runreconstruction__run__run_number=299929, user=user
        ),
    ]
    runs_list = [cert.runreconstruction.run.run_number for cert in certs]

    req = RequestFactory().get(reverse("summary:summary"))

    req.user = user

    resp = SummaryView.as_view()(req)
    assert resp.status_code == 200
    assert (
        TrackerCertification.objects.filter(
            runreconstruction__run__run_number__in=[355555, 299929]
        ).count()
        == 2
    )


def test_post_success():
    runs = [
        mixer.blend(OmsRun, run_number=355555),
        mixer.blend(OmsRun, run_number=299929),
    ]

    runs_list = [run.run_number for run in runs]
    form = SummaryExtraInfoForm(
        data={"runs_list": str(runs_list), "links_prompt_feedback": "link1, link2"}
    )
    assert form.is_valid()

    req = RequestFactory().post(reverse("summary:summary"), data=form.data)

    req.user = mixer.blend(User, user_privilege=User.SHIFTER)

    resp = SummaryView.as_view()(req)
    assert resp.status_code == 200
    result = json.loads(resp.content)
    assert result["success"] == True


def test_post_failure():

    form = SummaryExtraInfoForm(
        data={
            "runs_list": str([]),
        }
    )
    assert form.is_valid() == False

    req = RequestFactory().post(reverse("summary:summary"), data=form.data)

    req.user = mixer.blend(User, user_privilege=User.SHIFTER)

    resp = SummaryView.as_view()(req)
    assert resp.status_code == 200
    result = json.loads(resp.content)
    assert result["success"] == False
