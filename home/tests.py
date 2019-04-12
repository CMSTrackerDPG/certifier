import types

import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer

from home import views

pytestmark = pytest.mark.django_db

class TestHome:
    def test_home_view(self):
        req = RequestFactory().get("")
        resp = views.home(req)
        assert resp.status_code == 200
