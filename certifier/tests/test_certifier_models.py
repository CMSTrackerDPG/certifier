import pytest
from mixer.backend.django import mixer

from users.models import User
from certifier.models import *
from certifier.exceptions import (
    RunReconstructionIsAlreadyReference,
    RunReconstructionNotYetCertified,
)
from oms.models import OmsRun

pytestmark = pytest.mark.django_db


class TestRunReconstructionPromotion:
    """
    Test the promotion to reference procedure of RunReconstruction entries
    """

    def test_promote_reference_run_reco(self):
        """
        Try promoting a RunReconstruction that already is a refernce one
        """
        test_number = 323444
        runReconstruction = mixer.blend(
            RunReconstruction,
            run=mixer.blend(OmsRun, run_number=test_number),
            is_reference=True,
        )
        with pytest.raises(RunReconstructionIsAlreadyReference):
            runReconstruction.promote_to_reference()

    def test_promote_noncertified_run_reco(self):
        """
        Try promoting a RunReconstruction that has not been certified yet
        """
        test_number = 323444
        runReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number),
        )
        with pytest.raises(RunReconstructionNotYetCertified):
            runReconstruction.promote_to_reference()

    def test_promote_certified_run_reco(self):
        """
        Try promoting a RunReconstruction that has been certified
        """
        test_number = 323444
        # Make a new run reconstruction of type cosmics (not reference due to default value)
        runReconstruction = mixer.blend(
            RunReconstruction,
            run=mixer.blend(OmsRun, run_number=test_number, run_type="cosmics"),
        )
        # Blend up a GOOD certification for our lovely reconstruction
        trk_certification = mixer.blend(
            TrackerCertification,
            runreconstruction=runReconstruction,
            strip="good",
            tracking="good",
        )

        # Should promote just fine
        assert runReconstruction.promote_to_reference()


class TestRunReconstruction:
    def test_run_number(self):
        test_number = 323444
        runReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number)
        )
        assert runReconstruction.run_number == test_number

    def test_str_return(self):
        test_number = 323444
        test_reconstruction = "online"
        runReconstruction = mixer.blend(
            RunReconstruction,
            reconstruction=test_reconstruction,
            run=mixer.blend(OmsRun, run_number=test_number),
        )
        assert str(runReconstruction) == "{} {}".format(
            test_number, test_reconstruction
        )


class TestDataset:
    def test_name(self):
        test_dataset = "/test/test"
        dataset = mixer.blend(Dataset, dataset=test_dataset)
        assert str(dataset) == test_dataset


class TestPixelProblem:
    def test_name(self):
        test_problem = "test_problem_pixel"
        pixelProblem = mixer.blend(PixelProblem, name=test_problem)
        assert str(pixelProblem) == test_problem


class TestStripProblem:
    def test_name(self):
        test_problem = "test_problem_strip"
        stripProblem = mixer.blend(StripProblem, name=test_problem)
        assert str(stripProblem) == test_problem


class TestTrackingProblem:
    def test_name(self):
        test_problem = "test_problem_tracking"
        trackingProblem = mixer.blend(TrackingProblem, name=test_problem)
        assert str(trackingProblem) == test_problem


class TestBadReason:
    def test_name(self):
        test_reason = "test_reason"
        badReason = mixer.blend(BadReason, name=test_reason)
        assert str(badReason) == test_reason


class TestTrackerCertification:
    def test_run_number(self):
        test_number = 323444
        runReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number)
        )
        trackerCertification = mixer.blend(
            TrackerCertification, runreconstruction=runReconstruction
        )
        assert trackerCertification.run_number == test_number

    def test_reference_run_number(self):
        test_number = 323444
        referenceRunReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number)
        )
        trackerCertification = mixer.blend(
            TrackerCertification, reference_runreconstruction=referenceRunReconstruction
        )
        assert trackerCertification.reference_run_number == test_number

    def test_reconstruction(self):
        runReconstruction = mixer.blend(RunReconstruction, reconstruction="rereco")
        trackerCertification = mixer.blend(
            TrackerCertification, runreconstruction=runReconstruction
        )
        assert trackerCertification.reconstruction == "ReReco"

    def test_str_return(self):
        test_number = 323444
        runReconstruction = mixer.blend(RunReconstruction, reconstruction="rereco")
        referenceRunReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number)
        )
        trackerCertification = mixer.blend(
            TrackerCertification,
            reference_runreconstruction=referenceRunReconstruction,
            runreconstruction=runReconstruction,
        )
        assert str(trackerCertification) == "{} {} {}".format(
            runReconstruction,
            referenceRunReconstruction,
            trackerCertification.get_tracking_display(),
        )

    def test_is_bad(self):
        test_number = 323444
        runReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number)
        )
        trackerCertification = mixer.blend(
            TrackerCertification, runreconstruction=runReconstruction, strip="bad"
        )
        assert trackerCertification.is_bad is True

    def test_certification_same_user(self):
        """
        Same user can edit own certification
        """
        test_number = 323444
        user = mixer.blend(User)
        runReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number)
        )
        trackerCertification = mixer.blend(
            TrackerCertification, runreconstruction=runReconstruction, user=user
        )
        assert (
            TrackerCertification.can_be_certified_by_user(
                test_number, reconstruction=runReconstruction.reconstruction, user=user
            )
            is True
        )

    def test_certification_does_not_exist(self):
        """
        Non-existent certification should be certifiable
        """
        user = mixer.blend(User)
        assert (
            TrackerCertification.can_be_certified_by_user(
                354355, reconstruction="express", user=user
            )
            is True
        )

    def test_certification_different_user(self):
        """
        Different user cannot certify other's certification
        """
        test_number = 323444
        user_a = mixer.blend(User)
        user_b = mixer.blend(User)
        runReconstruction = mixer.blend(
            RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number)
        )
        trackerCertification = mixer.blend(
            TrackerCertification, runreconstruction=runReconstruction, user=user_a
        )
        assert (
            TrackerCertification.can_be_certified_by_user(
                test_number,
                reconstruction=runReconstruction.reconstruction,
                user=user_b,
            )
            is False
        )
