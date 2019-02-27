from django.db import models

from django.contrib.auth.models import AbstractUser

from oms.models import OmsRun


class User(AbstractUser):
    pass


class RunReconstruction(models.Model):
    RECONSTRUCTION_CHOICES = (
        ("online", "Online"),
        ("express", "Express"),
        ("prompt", "Prompt"),
        ("rereco", "ReReco"),
    )
    run = models.ForeignKey(OmsRun, on_delete=models.CASCADE)
    reconstruction = models.CharField(max_length=3, choices=RECONSTRUCTION_CHOICES)
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


class StripProblem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()


class TrackingProblem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()


class BadReason(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()


class RunCertification(models.Model):
    SUBCOMPONENT_STATUS_CHOICES = (("bad", "Bad"), ("good", "Good"), ("excluded", "Excluded"))

    runreconstruction = models.OneToOneField(
        RunReconstruction, on_delete=models.CASCADE, primary_key=True
    )
    reference_runrunreconstruction = models.ForeignKey(
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
        return self.run.run.run_number

    @property
    def reconstruction(self):
        return self.run.get_reconstruction_display()

    @property
    def reference_run_number(self):
        return self.reference_run.run.run_number

    def __str__(self):
        return "{} {} {}".format(
            self.run, self.reconstruction, self.get_tracking_display()
        )
