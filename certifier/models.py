from django.db import models
from users.models import User

from oms.models import OmsRun


class RunReconstruction(models.Model):
    RECONSTRUCTION_CHOICES = (
        ("online", "Online"),
        ("express", "Express"),
        ("prompt", "Prompt"),
        ("rereco", "ReReco"),
    )
    run = models.ForeignKey(OmsRun, on_delete=models.CASCADE)
    reconstruction = models.CharField(max_length=8, choices=RECONSTRUCTION_CHOICES)
    dataset = models.CharField(max_length=150)

    is_reference = models.BooleanField(default=False)

    class Meta:
        unique_together = ("run", "reconstruction")

    @property
    def run_number(self):
        return self.run.run_number

    def __str__(self):
        return "{} {}".format(self.run_number, self.reconstruction)


class PixelProblem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class StripProblem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class TrackingProblem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class BadReason(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class TrackerCertification(models.Model):
    SUBCOMPONENT_STATUS_CHOICES = (
        ("good", "Good"),
        ("bad", "Bad"),
        ("excluded", "Excluded"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    runreconstruction = models.OneToOneField(
        RunReconstruction, on_delete=models.CASCADE, primary_key=True
    )
    reference_runreconstruction = models.ForeignKey(
        RunReconstruction, on_delete=models.CASCADE, related_name="+"
    )

    pixel = models.CharField(max_length=3, choices=SUBCOMPONENT_STATUS_CHOICES)
    strip = models.CharField(max_length=3, choices=SUBCOMPONENT_STATUS_CHOICES)
    tracking = models.CharField(max_length=3, choices=SUBCOMPONENT_STATUS_CHOICES)

    pixel_lowstat = models.BooleanField(default=False)
    strip_lowstat = models.BooleanField(default=False)
    tracking_lowstat = models.BooleanField(default=False)

    pixel_problems = models.ManyToManyField(PixelProblem, blank=True)
    strip_problems = models.ManyToManyField(StripProblem, blank=True)
    tracking_problems = models.ManyToManyField(TrackingProblem, blank=True)

    bad_reason = models.ForeignKey(
        BadReason, null=True, blank=True, on_delete=models.SET_NULL
    )

    comment = models.TextField()

    @property
    def run_number(self):
        return self.runreconstruction.run.run_number

    @property
    def reconstruction(self):
        return self.runreconstruction.get_reconstruction_display()

    @property
    def reference_run_number(self):
        return self.reference_runreconstruction.run.run_number

    def __str__(self):
        return "{} {} {}".format(
            self.runreconstruction,
            self.reference_runreconstruction,
            self.get_tracking_display(),
        )
