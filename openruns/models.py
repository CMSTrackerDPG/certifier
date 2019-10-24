from django.db import models
from certifier.models import Dataset
from users.models import User

# Create your models here.

class OpenRuns(models.Model):
    STATE_CHOICES = (
        ("OPEN", "Open"),
        ("COMPLETED", "Completed"),
        ("SIGNOFF", "SignOff"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    run_number = models.PositiveIntegerField(
        help_text="Run number", verbose_name="Run", primary_key=True
    )

    dataset_express = models.CharField(max_length=150)
    dataset_prompt = models.CharField(max_length=150, null=True, blank=True)
    dataset_rereco = models.CharField(max_length=150, null=True, blank=True)
    dataset_rereco_ul = models.CharField(max_length=150, null=True, blank=True)

    date_retrieved = models.DateField()

    state_express = models.CharField(max_length=9, choices=STATE_CHOICES)
    state_prompt = models.CharField(max_length=9, choices=STATE_CHOICES)
    state_rereco = models.CharField(max_length=9, choices=STATE_CHOICES)
    state_rereco_ul = models.CharField(max_length=9, choices=STATE_CHOICES)

    def __str__(self):
        return "{}".format(self.run_number)
