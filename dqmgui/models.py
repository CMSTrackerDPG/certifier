from django.core.validators import validate_comma_separated_integer_list
from django.db import models

# Create your models here.
from crtfr.models import RunReconstruction


class Histogram(models.Model):
    """
    Stores summarizes of a DQM histogram retrieved from the jsonfairy
    """
    run_reconstruction = models.ForeignKey(RunReconstruction, on_delete=models.CASCADE)

    histogram_type = models.CharField(max_length=10)  # "TH1"
    title = models.CharField(max_length=100)  # "Digi ADC values"
    name = models.CharField(max_length=100)  # adc_PXBarrel
    entries = models.FloatField()  # ""
    x_mean = models.FloatField()  # ""
    x_rms = models.FloatField()  # ""
    x_label = models.CharField()  # "adc readout"
    x_min = models.FloatField()
    x_max = models.FloatField()
    bins_integral = models.FloatField()
    content = models.TextField(validators=[validate_comma_separated_integer_list], null=True, blank=True)
