import logging
from django.db import models
from users.models import User
from certifier.manager import TrackerCertificationManager
from oms.models import OmsRun
from delete.models import SoftDeletionModel
from certifier.exceptions import (
    RunReconstructionIsAlreadyReference,
    RunReconstructionNotYetCertified,
)

logger = logging.getLogger(__name__)


class RunReconstruction(models.Model):
    ONLINE = "online"
    EXPRESS = "express"
    PROMPT = "prompt"
    RERECO = "rereco"
    RERECOUL = "rerecoul"

    RECONSTRUCTION_CHOICES = (
        (ONLINE, "Online"),
        (EXPRESS, "Express"),
        (PROMPT, "Prompt"),
        (RERECO, "ReReco"),
        (RERECOUL, "ReRecoUL"),
    )
    run = models.ForeignKey(OmsRun, on_delete=models.CASCADE)
    reconstruction = models.CharField(max_length=8, choices=RECONSTRUCTION_CHOICES)

    is_reference = models.BooleanField(default=False)

    class Meta:
        unique_together = ("run", "reconstruction")
        ordering = ["-run__run_number"]

    @property
    def run_number(self):
        return self.run.run_number

    def promote_to_reference(self) -> bool:
        """
        Class method that, given a run number and a run reconstruction type,
        promotes it to reference run reconstruction if the following conditions
        apply:
        - The reconstruction is not already a reference
        - There is a TrackerCertification entry for this specific reconstruction
        - The certification is good

        Returns:
        True if successfully promoted reconstruction to reference, else raises custom
        exceptions:
        - RunReconstructionIsAlreadyReference if already a reference
        - RunReconstructionNotYetCertified if no certification found for this Run reco
        """

        if self.is_reference:
            raise RunReconstructionIsAlreadyReference(
                f"Run reconstruction {self.run_number}"
                f"({self.reconstruction}) is already a reference"
            )

        # Look into TrackerCertification for the specific run reconstruction
        # to see if it has been certified. RunReconstruction ids are TrackerCertification's
        # primary key
        if (
            TrackerCertification.objects.filter(runreconstruction=self).exists()
            and self.certification.is_good
        ):
            # Run reconstruction has been certified and is good,
            # so we're promoting it.
            self.is_reference = True
            self.save()
        else:
            raise RunReconstructionNotYetCertified(
                f"Run reconstruction {self.run_number}"
                f"({self.reconstruction}) has not been certified yet"
            )

        return True

    def __str__(self):
        return f"{self.run_number} {self.reconstruction}"


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

    GOOD = "good"
    BAD = "bad"
    EXCLUDED = "excluded"

    TRACKERMAP_EXISTS = "exists"
    TRACKERMAP_MISSING = "missing"

    # Incomplete status means missing data from RunRegistry,
    # OMS etc
    EXTERNAL_INFO_INCOMPLETE = "INC"
    EXTERNAL_INFO_COMPLETE = "COM"

    SUBCOMPONENT_STATUS_CHOICES = (
        (GOOD, "Good"),
        (BAD, "Bad"),
        (EXCLUDED, "Excluded"),
    )
    TRACKERMAP_CHOICES = (
        (TRACKERMAP_EXISTS, "Exists"),
        (TRACKERMAP_MISSING, "Missing"),
    )

    EXTERNAL_INFO_COMPLETENESS_CHOICES = (
        (EXTERNAL_INFO_INCOMPLETE, "Incomplete"),
        (EXTERNAL_INFO_COMPLETE, "Complete"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    runreconstruction = models.OneToOneField(
        RunReconstruction,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="certification",
    )

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True)

    reference_runreconstruction = models.ForeignKey(
        RunReconstruction,
        on_delete=models.CASCADE,
        related_name="ref",
        limit_choices_to={"is_reference": True},
    )

    trackermap = models.CharField(max_length=7, choices=TRACKERMAP_CHOICES)
    external_info_complete = models.BooleanField(
        help_text="OMS/RR Information completeness.", default=False
    )

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

    @classmethod
    def can_be_certified_by_user(
        cls, run_number: int, reconstruction: str, user: User
    ) -> bool:
        """
        Returns True if run_number/reconstruction combination certification does not exist
        OR exists and is certified by the user specified.

        Returns False if certification exists and is certified by another user.

        """
        try:
            certification = cls.objects.get(
                runreconstruction__run__run_number=run_number,
                runreconstruction__reconstruction=reconstruction,
            )
            # If shift leader, allow certification of any run
            if not user.has_shift_leader_rights and user != certification.user:
                return False

        except cls.DoesNotExist:
            # This specific certification does not exist yet
            pass

        return True

    @property
    def is_good(self):
        assert self.runreconstruction.run.run_type in ["cosmics", "collisions"]
        good_criteria = "good"
        candidates = [self.strip, self.tracking]
        candidates_lowstat = [self.strip_lowstat, self.tracking_lowstat]
        if self.runreconstruction.run.run_type == "collisions":
            candidates.append(self.pixel)
            candidates_lowstat.append(self.pixel_lowstat)

        for i in range(0, len(candidates)):
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
