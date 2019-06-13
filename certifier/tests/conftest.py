import pytest
from mixer.backend.django import mixer

from certifier.models import TrackerCertification

pytestmark = pytest.mark.django_db

@pytest.fixture
def some_certified_runs():
    """
    run     type       reco    good
    1       collisions express True
    2       collisions express True
    3       collisions express True
    4       collisions express True
    5       collisions express False
    6       collisions express False
    7       collisions express False
    1       collisions prompt  True
    3       collisions prompt  True
    4       collisions prompt  False
    5       collisions prompt  True
    6       collisions prompt  False
    10      cosmics    express True
    11      cosmics    express True
    12      cosmics    express True
    13      cosmics    express True
    14      cosmics    express True
    11      cosmics    prompt  True
    14      cosmics    prompt  False
    """

    # == collisions ==
    # == express ==
    # == Good ==
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=1, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=2, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=3, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=4, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="good",
    )

    # == Bad ==
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=5, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="bad",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=6, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="bad",
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=7, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="bad",
    )

    # == prompt ==
    # == Good ==
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=1, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=3, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=5, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="good",
        tracking="good",
    )

    # == Bad ==
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=4, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="good",
        strip="bad",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=6, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
        pixel="bad",
        strip="good",
        tracking="good",
    )

    # == cosmics ==
    # == express ==
    # == Good ==
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=10, run_type="cosmics", hlt_key="/physics")),
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=11, run_type="cosmics", hlt_key="/physics")),
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=12, run_type="cosmics", hlt_key="/physics")),
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=13, run_type="cosmics", hlt_key="/physics")),
        strip="good",
        tracking="good",
    )
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=14, run_type="cosmics", hlt_key="/physics")),
        strip="good",
        tracking="good",
    )

    # == prompt ==
    # == Good ==
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=11, run_type="cosmics", hlt_key="/physics")),
        strip="good",
        tracking="good",
    )
    # == Bad ==
    mixer.blend(
        "certifier.TrackerCertification",
        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=14, run_type="cosmics", hlt_key="/physics")),
        strip="bad",
        tracking="good",
    )

    assert 19 == len(TrackerCertification.objects.all())
    assert 12 == len(TrackerCertification.objects.filter(runreconstruction__run__run_type="collisions"))
    assert 7 == len(TrackerCertification.objects.filter(runreconstruction__run__run_type="cosmics"))

    assert 7 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="collisions", runreconstruction__reconstruction="express")
    )
    assert 5 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="collisions", runreconstruction__reconstruction="prompt")
    )

    assert 5 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="cosmics", runreconstruction__reconstruction="express")
    )
    assert 2 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="cosmics", runreconstruction__reconstruction="prompt")
    )

    assert 4 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="collisions", runreconstruction__reconstruction="express").good()
    )
    assert 3 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="collisions", runreconstruction__reconstruction="express").bad()
    )
    assert 3 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="collisions", runreconstruction__reconstruction="prompt").good()
    )
    assert 2 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="collisions", runreconstruction__reconstruction="prompt").bad()
    )

    assert 5 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="cosmics", runreconstruction__reconstruction="express").good()
    )
    assert 0 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="cosmics", runreconstruction__reconstruction="express").bad()
    )
    assert 1 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="cosmics", runreconstruction__reconstruction="prompt").good()
    )
    assert 1 == len(
        TrackerCertification.objects.filter(runreconstruction__run__run_type="cosmics", runreconstruction__reconstruction="prompt").bad()
    )

