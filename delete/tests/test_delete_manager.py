import pytest
from mixer.backend.django import mixer

from certifier.models import TrackerCertification

pytestmark = pytest.mark.django_db


class TestTrackerCertificationManager:
    def test_get_queryset(self):
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=123456)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=234567)))

        assert len(TrackerCertification.objects.all()) == 2
        assert len(TrackerCertification.all_objects.all()) == 2
        TrackerCertification.objects.all().delete()
        assert TrackerCertification.objects.exists() is False
        assert TrackerCertification.all_objects.exists() is True

    def test_alive_only(self):
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=123456)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=234567)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=345678)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=456789)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=567890)))

        assert len(TrackerCertification.objects.all()) == 5

        TrackerCertification.objects.filter(runreconstruction__run__run_number__gt=300000).delete()

        assert len(TrackerCertification.objects.all()) == 2
        assert len(TrackerCertification.objects.all().alive()) == 2
        assert len(TrackerCertification.objects.all().dead()) == 0
        assert len(TrackerCertification.all_objects.all()) == 5
        assert len(TrackerCertification.all_objects.all().alive()) == 2
        assert len(TrackerCertification.all_objects.all().dead()) == 3

        TrackerCertification.all_objects.filter(runreconstruction__run__run_number__gt=300000).dead().restore()
        assert len(TrackerCertification.objects.all()) == 5
        assert len(TrackerCertification.all_objects.all()) == 5
        assert len(TrackerCertification.all_objects.all().alive()) == 5
        assert len(TrackerCertification.all_objects.all().dead()) == 0

    def test_dead(self):
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=123456)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=234567)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=345678)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=456789)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=567890)))

        assert len(TrackerCertification.objects.all()) == 5

        TrackerCertification.objects.filter(runreconstruction__run__run_number__gt=300000).delete()

        assert len(TrackerCertification.objects.get_queryset()) == 2
        assert len(TrackerCertification.all_objects.get_queryset()) == 5
        assert len(TrackerCertification.objects.alive()) == 2
        assert len(TrackerCertification.objects.dead()) == 0
