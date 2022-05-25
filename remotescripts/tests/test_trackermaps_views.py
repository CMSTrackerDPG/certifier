import logging
import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import PermissionDenied
from users.models import User
from remotescripts.views import TrackerMapsView
from mixer.backend.django import mixer

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.django_db


class TestTrackermapsJSONResponses:
    def test_trackermap_generation_view(self):
        """
        Try requesting an invalid array of run numbers
        This is done with POST via an XMLHttpRequest.
        """
        # Use an invalid string in list
        arguments = {"type": "StreamExpress", "list": "299329-5555"}
        req = RequestFactory().post(
            reverse("remotescripts:trackermaps"),
            data=arguments,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        # Shifters and up should be able to access this
        req.user = mixer.blend(User, user_privilege=User.SHIFTER)
        resp = TrackerMapsView.as_view()(req)
        assert resp.status_code == 400

        # Non-shiftleader should get error
        req.user = mixer.blend(User, user_privilege=User.GUEST)
        with pytest.raises(PermissionDenied):
            resp = TrackerMapsView.as_view()(req)

        # Cannot test valid tracker maps generation,
        # since CI environment has no access to vocms066
