import pytest
from mixer.backend.django import mixer

from certifier.models import TrackerCertification

pytestmark = pytest.mark.django_db

def test_delete():
    run = mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=123456)))

    assert TrackerCertification.objects.filter(runreconstruction__run__run_number=123456).exists() is True
    assert run.runreconstruction.run.run_number == 123456
    run.delete()
    assert TrackerCertification.objects.filter(runreconstruction__run__run_number=123456).exists() is False
    assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=123456).exists() is True
    assert TrackerCertification.all_objects.get(runreconstruction__run__run_number=123456).pk == run.pk
    run.restore()
    assert TrackerCertification.objects.filter(runreconstruction__run__run_number=123456).exists() is True
    assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=123456).exists() is True
    run.hard_delete()
    assert TrackerCertification.objects.filter(runreconstruction__run__run_number=123456).exists() is False
    assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=123456).exists() is False

    run = mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=234567)))
    assert run.runreconstruction.run.run_number == 234567
    TrackerCertification.all_objects.get_queryset().hard_delete()
    assert TrackerCertification.objects.filter(runreconstruction__run__run_number=123456).exists() is False
    assert TrackerCertification.all_objects.filter(runreconstruction__run__run_number=123456).exists() is False
