import logging
import pytest
from django.test import RequestFactory
from django.urls import reverse
from trackermaps.views import maps

logger = logging.getLogger(__name__)


class TestTrackermapsJSONResponses:
    def test_400_response(self):
        """
        Try requesting an invalid array of run numbers
        This is done with POST via an XMLHttpRequest.
        """
        # Use an invalid string in list
        arguments = {'type': 'StreamExpress', 'list': '299329-5555'}
        req = RequestFactory().post(reverse('trackermaps:maps'),
                                    data=arguments,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        resp = maps(req)
        assert resp.status_code == 400
