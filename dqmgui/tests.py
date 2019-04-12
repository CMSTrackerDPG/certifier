from django.test import TestCase

# Create your tests here.
import pytest
from certifier.models import RunReconstruction
from dqmgui.models import Histogram
from oms.models import OmsRun
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestHistogram:
    def test_histogram_creation(self):
        assert Histogram.objects.count() == 0

        test_number=323444
        test_reconstruction="online"
        runReconstruction = mixer.blend(RunReconstruction, reconstruction=test_reconstruction, run=mixer.blend(OmsRun, run_number=test_number))

        kwargs = {
            "run_reconstruction": runReconstruction,
            "title": "Digi ADC values",
            "name": "adc_PXBarrel",
            "entries": 12354.0,
            "x_mean": 123,
            "x_rms": 456,
            "x_label": "adc readout",
            "x_min": 12,
            "x_max": 987,
            "bins_integral": 123456
        }
        histogram = Histogram(**kwargs)
        histogram.save()
        assert Histogram.objects.count() == 1
