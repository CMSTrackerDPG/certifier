import pytest
from mixer.backend.django import mixer

from certifier.models import TrackerCertification

pytestmark = pytest.mark.django_db

@pytest.fixture
def runs_with_three_refs():
    runreconstruction_ref12=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=12), is_reference=True)
    runreconstruction_ref1=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=1), is_reference=True)
    runreconstruction_ref2=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=2), is_reference=True)
    runreconstruction_ref3=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=3), is_reference=True)
    runreconstruction_ref4=mixer.blend("certifier.RunReconstruction", is_reference=True)

    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref1)
    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref2)
    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref3)
    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref2)
    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref3)
    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref2)
    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref1)
    mixer.blend("certifier.TrackerCertification", reference_runreconstruction=runreconstruction_ref1)

@pytest.fixture
def runs_for_slr():
    """
    Certified runs used to test the shift leader report
    """
    conditions = [
        ["cosmics", "express", 0.1234, 72, "2018-05-14", "good", "/cdaq/dsdadasphysics"],
        ["collisions", "prompt", 1.234, 5432, "2018-05-14", "bad", "/cdaq/physics"],  #######
        ["cosmics", "prompt", 0, 25, "2018-05-14", "bad", "/cdaq/phydasdsics"],  ########
        ["collisions", "express", 423.24, 2, "2018-05-15", "good", "/cdaq/physics"],
        ["collisions", "express", 0, 72, "2018-05-14", "good", "/cdaq/physics"],
        ["cosmics", "express", 0, 12, "2018-05-17", "good", "/cdaq/pdsadashysics"],
        ["cosmics", "express", 0, 72, "2018-05-17", "bad", "/cdaq/phdasdsysics"],
        ["cosmics", "express", 0, 42, "2018-05-14", "bad", "/cdaq/phydsdassics"],  #######
        ["collisions", "express", 124.123, 72, "2018-05-18", "good", "/cdaq/physics"],
        ["cosmics", "express", 0, 1242, "2018-05-14", "good", "/cdaq/phydsdassics"],
        ["cosmics", "express", 0, 72, "2018-05-20", "good", "/cdaq/physdsadsaics"],
        ["collisions", "express", 999, 142, "2018-05-20", "good", "/cdaq/physics"],
        ["collisions", "prompt", 0, 72, "2018-05-20", "bad", "/cdaq/physics"],  #######
        ["collisions", "prompt", 123132.32, 4522, "2018-05-20", "bad", "/cdaq/physics"],  #######
        ["collisions", "express", 0, 72, "2018-05-20", "good", "/cdaq/physics"],
        ["collisions", "express", -1, 71232, "2018-05-14", "good", "/cdaq/physics"],
        ["cosmics", "express", 0, 712, "2018-05-17", "good", "/cdaq/phdsadasysics"],
        ["collisions", "express", 5213, 142, "2018-05-14", "good", "/cdaq/physics"],
        ["collisions", "express", 154543, 72, "2018-05-18", "good", "/cdaq/physics"],
    ]

    for condition in conditions:
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=condition[1], run=mixer.blend("oms.OmsRun", run_type=condition[0], recorded_lumi=condition[2], lumisections=condition[3], hlt_key=condition[6], stable_beam=True)),
            date=condition[4],
            pixel=condition[5],
            strip=condition[5],
            tracking=condition[5],
        )

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

@pytest.fixture
def legitimate_reference_runs():
    """
    Reference runs as they might be used in production
    """
    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend("oms.OmsRun", run_number=300100, run_type="collisions", stable_beam=True, hlt_key="/cdaq/physics", b_field="3.8 T", energy="13 TeV", fill_type_party1="Proton-Proton")
        reconstruction="express",
        dataset=mixer.blend("certifier.Dataset", dataset="/StreamExpress/Run2018A-Express-v1/DQMIO")
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend("oms.OmsRun", run_number=300101, run_type="collisions", stable_beam=True, hlt_key="/cdaq/physics", b_field="3.8 T", energy="13 TeV", fill_type_party1="Proton-Proton")
        reconstruction="express",
        dataset=mixer.blend("certifier.Dataset", dataset="/StreamExpress/Run2018A-Express-v1/DQMIO")
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend("oms.OmsRun", run_number=300150, run_type="collisions", stable_beam=True, hlt_key="/cdaq/physics", b_field="3.8 T", energy="13 TeV", fill_type_party1="Proton-Proton")
        reconstruction="prompt",
        dataset=mixer.blend("certifier.Dataset", dataset="/ZeroBias/Run2018D-PromptReco-v2/DQMIO")
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend("oms.OmsRun", run_number=300200, run_type="cosmics", b_field="3.8 T", energy="Cosmics", fill_type_party1="Cosmics")
        reconstruction="express",
        dataset=mixer.blend("certifier.Dataset", dataset="/StreamExpressCosmics/Run2018D-Express-v1/DQMIO")
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend("oms.OmsRun", run_number=300250, run_type="cosmics", b_field="3.8 T", energy="Cosmics", fill_type_party1="Cosmics")
        reconstruction="prompt",
        dataset=mixer.blend("certifier.Dataset", dataset="/Cosmics/Run2018D-PromptReco-v2/DQMIO")
    )

@pytest.fixture
def legitimate_types():
    """
    Types as they might be used in production
    """
    mixer.blend(
        "certifier.RunReconstruction",
        run=mixer.blend("oms.OmsRun", run_type="collisions", stable_beam=True, hlt_key="/cdaq/physics", b_field="3.8 T", energy="13 TeV", fill_type_party1="Proton-Proton")
        reconstruction="express",
        dataset=mixer.blend("certifier.Dataset", dataset="/StreamExpress/Run2018A-Express-v1/DQMIO")
    )

    mixer.blend(
        "certifier.RunReconstruction",
        run=mixer.blend("oms.OmsRun", run_type="collisions", stable_beam=True, hlt_key="/cdaq/physics", b_field="3.8 T", energy="13 TeV", fill_type_party1="Proton-Proton")
        reconstruction="prompt",
        dataset=mixer.blend("certifier.Dataset", dataset="/ZeroBias/Run2018D-PromptReco-v2/DQMIO")
    )

    mixer.blend(
        "certifier.RunReconstruction",
        run=mixer.blend("oms.OmsRun", run_type="cosmics", b_field="3.8 T", energy="Cosmics", fill_type_party1="Cosmics")
        reconstruction="express",
        dataset=mixer.blend("certifier.Dataset", dataset="/StreamExpressCosmics/Run2018D-Express-v1/DQMIO")
    )

    mixer.blend(
        "certifier.RunReconstruction",
        run=mixer.blend("oms.OmsRun", run_type="cosmics", b_field="3.8 T", energy="Cosmics", fill_type_party1="Cosmics")
        reconstruction="prompt",
        dataset=mixer.blend("certifier.Dataset", dataset="/Cosmics/Run2018D-PromptReco-v2/DQMIO")
    )

@pytest.fixture
def runs_for_summary_report(legitimate_types, legitimate_reference_runs):
    """
    Certified runs for the current day.
    Used to test the summary report.

    All runs will be assigned to the first User that exists.

    Code was partially generated via print_mixer_code() helper in utilities.py
    """
    types = Type.objects.all()
    t1 = types.filter(runtype="Collisions", reco="Express")[0]
    t2 = types.filter(runtype="Collisions", reco="Prompt")[0]
    t3 = types.filter(runtype="Cosmics", reco="Express")[0]
    t4 = types.filter(runtype="Cosmics", reco="Prompt")[0]

    ref_runs = ReferenceRun.objects.all()
    r1 = ref_runs.filter(runtype="Collisions", reco="Express")[0]
    r2 = ref_runs.filter(runtype="Collisions", reco="Prompt")[0]
    r3 = ref_runs.filter(runtype="Cosmics", reco="Express")[0]
    r4 = ref_runs.filter(runtype="Cosmics", reco="Prompt")[0]

    today = timezone.now().date

    user = User.objects.first()

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300024",
        type=t4,
        reference_run=r4,
        trackermap="Missing",
        number_of_ls="372",
        int_luminosity="0.00",
        pixel="Lowstat",
        sistrip="Lowstat",
        tracking="Excluded",
        date=today,
        comment="""Water specific forget carry week. Likely 
                friend claim marriage. White long design. Drop daughter free free 
                analysis hang what run. Hospital administration one while the call.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300023",
        type=t3,
        reference_run=r3,
        trackermap="Exists",
        number_of_ls="207",
        int_luminosity="0.00",
        pixel="Good",
        sistrip="Good",
        tracking="Bad",
        date=today,
        comment="""Her arrive course management training probably anyone.
    Thank cut right manage enough state lose.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300022",
        type=t2,
        reference_run=r2,
        trackermap="Missing",
        number_of_ls="74",
        int_luminosity="874.62",
        pixel="Excluded",
        sistrip="Excluded",
        tracking="Lowstat",
        date=today,
        comment="""After weight institution whose produce. End 
                away finish anything voice. Turn worker success rather argue. Animal 
                right music material. Development clear suddenly bank send central 
                wall.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300021",
        type=t3,
        reference_run=r3,
        trackermap="Missing",
        number_of_ls="367",
        int_luminosity="0.00",
        pixel="Good",
        sistrip="Bad",
        tracking="Excluded",
        date=today,
        comment="""Still a usually member quite many cause. Summer now finish 
                may anything. Best hang light spend happen. Accept idea if should 
                possible ball official.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300020",
        type=t2,
        reference_run=r2,
        trackermap="Exists",
        number_of_ls="793",
        int_luminosity="572.98",
        pixel="Excluded",
        sistrip="Lowstat",
        tracking="Bad",
        date=today,
        comment="""Part by fight such policy candidate cold. Happy career 
                hope who. 
                
                Apply around seem win dog. Walk shot far record decade 
                message trouble.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300019",
        type=t2,
        reference_run=r2,
        trackermap="Missing",
        number_of_ls="520",
        int_luminosity="433.99",
        pixel="Excluded",
        sistrip="Good",
        tracking="Excluded",
        date=today,
        comment="""Nor particular them win share fire agree. Job kind offer 
                war lawyer couple card. Young degree go thus whether including away 
                on.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300018",
        type=t1,
        reference_run=r1,
        trackermap="Exists",
        number_of_ls="242",
        int_luminosity="983.49",
        pixel="Excluded",
        sistrip="Lowstat",
        tracking="Bad",
        date=today,
        comment="""Attack strategy raise smile and. West but alone position 
                ago finish change. Another message computer blood provide else 
                hard.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300017",
        type=t4,
        reference_run=r4,
        trackermap="Missing",
        number_of_ls="142",
        int_luminosity="0.00",
        pixel="Excluded",
        sistrip="Good",
        tracking="Bad",
        date=today,
        comment="""Employee hard hard cost near enter recent. Remember plan 
                hang.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300016",
        type=t2,
        reference_run=r2,
        trackermap="Exists",
        number_of_ls="188",
        int_luminosity="391.13",
        pixel="Excluded",
        sistrip="Good",
        tracking="Bad",
        date=today,
        comment="""Why before work contain these indicate seem. None clear 
                pass near minute once. Surface floor focus car number high still. 
                Western trial collection evidence prepare.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300015",
        type=t2,
        reference_run=r2,
        trackermap="Missing",
        number_of_ls="265",
        int_luminosity="432.73",
        pixel="Lowstat",
        sistrip="Lowstat",
        tracking="Lowstat",
        date=today,
        comment="""Better private while allow example style. Activity along 
                me effort. Exactly thing commercial hang. Course shake red son source 
                anything.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300014",
        type=t2,
        reference_run=r2,
        trackermap="Exists",
        number_of_ls="164",
        int_luminosity="836.49",
        pixel="Excluded",
        sistrip="Good",
        tracking="Excluded",
        date=today,
        comment="""Might surface line shoulder fund institution. 
                Factor pretty or sign benefit ten. Stock study nation bill. Use image 
                kitchen establish explain eye north still. Anyone news fight huge 
                region.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300013",
        type=t2,
        reference_run=r2,
        trackermap="Missing",
        number_of_ls="642",
        int_luminosity="138.83",
        pixel="Good",
        sistrip="Lowstat",
        tracking="Excluded",
        date=today,
        comment="""Bill suggest success new citizen. Clear apply already rich 
                cultural mouth support. Parent their case some win your news. Garden 
                wear body into character. Age security including later involve.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300012",
        type=t4,
        reference_run=r4,
        trackermap="Exists",
        number_of_ls="365",
        int_luminosity="0.00",
        pixel="Bad",
        sistrip="Bad",
        tracking="Bad",
        date=today,
        comment="""Care agree might TV paper response. Future support 
                certainly follow thousand network. Positive cell raise no property 
                science. Economic suffer market trade politics region huge.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300011",
        type=t1,
        reference_run=r1,
        trackermap="Missing",
        number_of_ls="826",
        int_luminosity="621.59",
        pixel="Excluded",
        sistrip="Lowstat",
        tracking="Bad",
        date=today,
        comment="""Serious character against water. With customer product 
                different. Understand heart civil main sit. Best set baby. 
                Traditional person picture create love maybe. Another his compare 
                gas.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300010",
        type=t1,
        reference_run=r1,
        trackermap="Missing",
        number_of_ls="378",
        int_luminosity="786.43",
        pixel="Excluded",
        sistrip="Bad",
        tracking="Excluded",
        date=today,
        comment="""Contain many the into television. Finally age little 
                treat. Note PM mention how oh assume wrong. Inside listen health. Off 
                degree how economy scientist.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300009",
        type=t3,
        reference_run=r3,
        trackermap="Exists",
        number_of_ls="134",
        int_luminosity="0.00",
        pixel="Lowstat",
        sistrip="Good",
        tracking="Lowstat",
        date=today,
        comment="""Turn drug science practice. Drop four budget section. Into 
                draw more rock create pretty democratic. Really clear determine 
                agreement foreign already him.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300008",
        type=t4,
        reference_run=r4,
        trackermap="Missing",
        number_of_ls="356",
        int_luminosity="0.00",
        pixel="Lowstat",
        sistrip="Bad",
        tracking="Good",
        date=today,
        comment="""Try billion collection lose. Site near thank class yard 
                major. Test anyone much either exactly candidate east. Hit force oh 
                professional network wide during fear. Pick figure young 
                television.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300007",
        type=t4,
        reference_run=r4,
        trackermap="Missing",
        number_of_ls="341",
        int_luminosity="0.00",
        pixel="Lowstat",
        sistrip="Lowstat",
        tracking="Lowstat",
        date=today,
        comment="""Yard central myself leg sit. Consumer remember fund 
                control then. Even near see girl hit season.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300006",
        type=t2,
        reference_run=r2,
        trackermap="Missing",
        number_of_ls="399",
        int_luminosity="954.85",
        pixel="Excluded",
        sistrip="Excluded",
        tracking="Bad",
        date=today,
        comment="""Training adult impact treatment die military. Glass cost 
                experience various rather anything human. Either gas area may and 
                any.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300005",
        type=t1,
        reference_run=r1,
        trackermap="Exists",
        number_of_ls="981",
        int_luminosity="510.75",
        pixel="Good",
        sistrip="Excluded",
        tracking="Bad",
        date=today,
        comment="""Enter quality material once rule with bill wind. Far whole 
                give run. Government authority many wish sport.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300004",
        type=t3,
        reference_run=r3,
        trackermap="Missing",
        number_of_ls="441",
        int_luminosity="0.00",
        pixel="Excluded",
        sistrip="Bad",
        tracking="Bad",
        date=today,
        comment="""Notice in affect information value carry. Great success 
                which on. Nation join doctor event. Actually local economy positive. 
                Left woman effort technology reality. Military you it.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300003",
        type=t3,
        reference_run=r3,
        trackermap="Missing",
        number_of_ls="574",
        int_luminosity="0.00",
        pixel="Lowstat",
        sistrip="Lowstat",
        tracking="Good",
        date=today,
        comment="""Ball west movie pain enough. Child tonight guy hotel 
                knowledge. Of everything past language heavy general. Goal option 
                probably prevent. Wonder general difference design test.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300002",
        type=t2,
        reference_run=r2,
        trackermap="Exists",
        number_of_ls="873",
        int_luminosity="273.88",
        pixel="Good",
        sistrip="Excluded",
        tracking="Bad",
        date=today,
        comment="""Important front more because nation check. Shoot accept 
                seem detail stand under. Poor shoot next admit close conference. Put 
                research watch mind.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300001",
        type=t2,
        reference_run=r2,
        trackermap="Exists",
        number_of_ls="834",
        int_luminosity="840.18",
        pixel="Good",
        sistrip="Excluded",
        tracking="Lowstat",
        date=today,
        comment="""Vote kind rule loss dark course. Across difficult people shoot.
    Thought real yeah improve. Explain media book yes business east.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300001",
        type=t1,
        reference_run=r1,
        trackermap="Exists",
        number_of_ls="997",
        int_luminosity="632.57",
        pixel="Bad",
        sistrip="Excluded",
        tracking="Excluded",
        date=today,
        comment="""Develop should across truth prevent single. Thus this much 
                method child. Population impact accept black drop say. Game thought 
                senior.""",
    )

    mixer.blend(
        "certhelper.RunInfo",
        userid=user,
        run_number="300000",
        type=t4,
        reference_run=r4,
        trackermap="Exists",
        number_of_ls="856",
        int_luminosity="0.00",
        pixel="Good",
        sistrip="Lowstat",
        tracking="Bad",
        date=today,
        comment="""Notice this resource center. Interest remain throughout 
                condition contain save problem. Town treatment magazine environmental 
                report all rule.""",
    )

