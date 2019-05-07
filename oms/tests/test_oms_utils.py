import types

import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer

from users.views import *

pytestmark = pytest.mark.django_db

