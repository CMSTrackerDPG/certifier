import logging
import pytest
from django.test import RequestFactory
from django.urls import reverse
from users.models import User
from trackermaps.views import maps
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
        arguments = {'type': 'StreamExpress', 'list': '299329-5555'}
        req = RequestFactory().post(reverse('trackermaps:maps'),
                                    data=arguments,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # Only shiftleaders should access this
        req.user = mixer.blend(User, user_privilege=User.SHIFTLEADER)
        resp = maps(req)
        assert resp.status_code == 400

        # Non-shiftleader should get error
        req.user = mixer.blend(User, user_privilege=User.SHIFTER)
        resp = maps(req)
        assert resp.status_code == 302
