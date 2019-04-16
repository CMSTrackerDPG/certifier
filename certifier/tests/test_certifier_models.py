import pytest
from mixer.backend.django import mixer

from certifier.models import *
from oms.models import OmsRun

pytestmark = pytest.mark.django_db

class TestRunReconstruction:
    def test_run_number(self):
        test_number=323444
        runReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number))
        assert runReconstruction.run_number == test_number

    def test_str_return(self):
        test_number=323444
        test_reconstruction="online"
        runReconstruction = mixer.blend(RunReconstruction, reconstruction=test_reconstruction, run=mixer.blend(OmsRun, run_number=test_number))
        assert str(runReconstruction) == "{} {}".format(test_number, test_reconstruction)

class TestDataset:
    def test_name(self):
        test_dataset="/test/test"
        dataset = mixer.blend(Dataset, dataset=test_dataset)
        assert str(dataset) == test_dataset

class TestPixelProblem:
    def test_name(self):
        test_problem="test_problem_pixel"
        pixelProblem = mixer.blend(PixelProblem, name=test_problem)
        assert str(pixelProblem) == test_problem

class TestStripProblem:
    def test_name(self):
        test_problem="test_problem_strip"
        stripProblem = mixer.blend(StripProblem, name=test_problem)
        assert str(stripProblem) == test_problem

class TestTrackingProblem:
    def test_name(self):
        test_problem="test_problem_tracking"
        trackingProblem = mixer.blend(TrackingProblem, name=test_problem)
        assert str(trackingProblem) == test_problem

class TestBadReason:
    def test_name(self):
        test_reason="test_reason"
        badReason = mixer.blend(BadReason, name=test_reason)
        assert str(badReason) == test_reason

class TestTrackerCertification:
    def test_run_number(self):
        test_number=323444
        runReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number))
        trackerCertification = mixer.blend(TrackerCertification, runreconstruction=runReconstruction)
        assert trackerCertification.run_number == test_number

    def test_reference_run_number(self):
        test_number=323444
        referenceRunReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number))
        trackerCertification = mixer.blend(TrackerCertification, reference_runreconstruction=referenceRunReconstruction)
        assert trackerCertification.reference_run_number == test_number

    def test_reconstruction(self):
        runReconstruction = mixer.blend(RunReconstruction, reconstruction="rereco")
        trackerCertification = mixer.blend(TrackerCertification, runreconstruction=runReconstruction)
        assert trackerCertification.reconstruction == "ReReco"

    def test_str_return(self):
        test_number=323444
        runReconstruction = mixer.blend(RunReconstruction, reconstruction="rereco")
        referenceRunReconstruction = mixer.blend(RunReconstruction, run=mixer.blend(OmsRun, run_number=test_number))
        trackerCertification = mixer.blend(TrackerCertification, reference_runreconstruction=referenceRunReconstruction, runreconstruction=runReconstruction)
        assert str(trackerCertification) == "{} {} {}".format(runReconstruction, referenceRunReconstruction, trackerCertification.get_tracking_display())
