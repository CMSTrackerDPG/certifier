from django.db import models
from users.models import User
from certifier.manager import *
from oms.models import OmsRun
from delete.models import SoftDeletionModel

class RunReconstruction(models.Model):
    RECONSTRUCTION_CHOICES = (
        ("online", "Online"),
        ("express", "Express"),
        ("prompt", "Prompt"),
        ("rereco", "ReReco"),
        ("rerecoul", "ReRecoUL"),
    )
    run = models.ForeignKey(OmsRun, on_delete=models.CASCADE)
    reconstruction = models.CharField(max_length=8, choices=RECONSTRUCTION_CHOICES)

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

class Dataset(models.Model):
    dataset = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.dataset


class TrackerCertification(SoftDeletionModel):
    objects = TrackerCertificationManager()
    all_objects = TrackerCertificationManager(alive_only=False)

    SUBCOMPONENT_STATUS_CHOICES = (
        ("good", "Good"),
        ("bad", "Bad"),
        ("excluded", "Excluded"),
    )
    TRACKERMAP_CHOICES = (("exists", "Exists"), ("missing", "Missing"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    runreconstruction = models.OneToOneField(
        RunReconstruction, on_delete=models.CASCADE, primary_key=True
    )

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    reference_runreconstruction = models.ForeignKey(
        RunReconstruction, on_delete=models.CASCADE, related_name="ref", limit_choices_to={'is_reference': True}
    )

    trackermap = models.CharField(max_length=7, choices=TRACKERMAP_CHOICES)

    pixel = models.CharField(max_length=8, choices=SUBCOMPONENT_STATUS_CHOICES)
    strip = models.CharField(max_length=8, choices=SUBCOMPONENT_STATUS_CHOICES)
    tracking = models.CharField(max_length=8, choices=SUBCOMPONENT_STATUS_CHOICES)

    pixel_lowstat = models.BooleanField(default=False)
    strip_lowstat = models.BooleanField(default=False)
    tracking_lowstat = models.BooleanField(default=False)

    pixel_problems = models.ManyToManyField(PixelProblem, blank=True)
    strip_problems = models.ManyToManyField(StripProblem, blank=True)
    tracking_problems = models.ManyToManyField(TrackingProblem, blank=True)

    bad_reason = models.ForeignKey(
        BadReason, null=True, blank=True, on_delete=models.SET_NULL
    )

    date = models.DateField()

    comment = models.TextField(blank=True)

    @property
    def is_good(self):
        assert self.runreconstruction.run.run_type in ["cosmics", "collisions"]
        good_criteria = "good"
        candidates = [self.strip, self.tracking]
        candidates_lowstat = [self.strip_lowstat, self.tracking_lowstat]
        if self.runreconstruction.run.run_type == "collisions":
            candidates.append(self.pixel)
            candidates_lowstat.append(self.pixel_lowstat)

        for i in range(0,len(candidates)):
            if candidates[i] != good_criteria and candidates_lowstat[i] != "lowstat":
                return False
        return True

    @property
    def is_bad(self):
        return not self.is_good

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
