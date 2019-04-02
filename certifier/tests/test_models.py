import pytest
from mixer.backend.django import mixer

from certifier.models import *

pytestmark = pytest.mark.django_db

class TestRunReconstruction:
    def test_init(self):
        obj = mixer.blend(RunReconstruction, reconstruction="online")
        assert obj.pk == 1
        assert obj.__class__.__name__ == "RunReconstruction"

class TestPixelProblem:
    def test_init(self):
        obj = mixer.blend(PixelProblem)
        assert obj.pk == 1
        assert obj.__class__.__name__ == "PixelProblem"

class TestStripProblem:
    def test_init(self):
        obj = mixer.blend(StripProblem)
        assert obj.pk == 1
        assert obj.__class__.__name__ == "StripProblem"

class TestTrackingProblem:
    def test_init(self):
        obj = mixer.blend(TrackingProblem)
        assert obj.pk == 1
        assert obj.__class__.__name__ == "TrackingProblem"

class BadReason:
    def test_init(self):
        obj = mixer.blend(BadReason)
        assert obj.pk == 1
        assert obj.__class__.__name__ == "BadReason"

class TrackerCertification:
    def test_init(self):
        obj = mixer.blend(TrackerCertification)
        assert obj.pk == 1
        assert obj.__class__.__name__ == "TrackerCertification"


