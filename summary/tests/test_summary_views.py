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
    """
    GETting the page should result in creation of SummaryInfo instances
    """

    user = mixer.blend(User, user_privilege=User.SHIFTER)
    certs = [
        mixer.blend(
            TrackerCertification, runreconstruction__run__run_number=355555, user=user
        ),
        mixer.blend(
            TrackerCertification, runreconstruction__run__run_number=299929, user=user
        ),
    ]
    certs_list = [cert.runreconstruction.pk for cert in certs]

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
    """
    Successful post of summary info
    """
    certs = [
        mixer.blend(TrackerCertification, runreconstruction__run__run_number=355555),
        mixer.blend(TrackerCertification, runreconstruction__run__run_number=299929),
    ]

    certs_list = [cert.runreconstruction.pk for cert in certs]
    form = SummaryExtraInfoForm(
        data={"certs_list": str(certs_list), "links_prompt_feedback": "link1, link2"}
    )
    assert form.is_valid()

    req = RequestFactory().post(reverse("summary:summary"), data=form.data)

    req.user = mixer.blend(User, user_privilege=User.SHIFTER)

    resp = SummaryView.as_view()(req)
    assert resp.status_code == 200
    result = json.loads(resp.content)
    assert result["success"] == True


def test_post_failure():
    """
    Not supplying links_prompt_feedback is not allowed
    """
    form = SummaryExtraInfoForm(
        data={
            "certs_list": str([]),
        }
    )
    assert form.is_valid() == False

    req = RequestFactory().post(reverse("summary:summary"), data=form.data)

    req.user = mixer.blend(User, user_privilege=User.SHIFTER)

    resp = SummaryView.as_view()(req)
    assert resp.status_code == 200
    result = json.loads(resp.content)
    assert result["success"] == False
