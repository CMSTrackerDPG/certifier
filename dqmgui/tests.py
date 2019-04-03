'''
from django.test import TestCase

# Create your tests here.
from certifier.models import RunReconstruction
from dqmgui.models import Histogram

class TestHistogram:
    def test_histogram_creation(self):
        assert Histogram.objects.count() == 0

        run_number = 321123
        reconstruction = "express"
        run = RunReconstruction.objects.get(run_number =run_number, reconstruction=reconstruction)

        kwargs = {
            "run_reconstruction": run,
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
'''
