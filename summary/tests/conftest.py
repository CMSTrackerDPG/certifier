import pytest
from mixer.backend.django import mixer

from django.utils import timezone
from django.contrib.auth import get_user_model
from certifier.models import TrackerCertification, RunReconstruction, Dataset
from utilities.credentials import (
    SUPERUSER_USERNAME,
    PASSWORD,
    SHIFTER1_USERNAME,
    SHIFTER2_USERNAME,
    SHIFTLEADER_USERNAME,
    EXPERT_USERNAME,
    ADMIN_USERNAME,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def shifter(django_user_model):
    user = mixer.blend(get_user_model(), username=SHIFTER1_USERNAME, password=PASSWORD)
    user.extra_data = {"cern_roles": ["shifter"]}
    user.update_privilege()
    user.save()
    return user


@pytest.fixture
def legitimate_reference_runs():
    """
    Reference runs as they might be used in production
    """
    dataset1 = mixer.blend(
        "certifier.Dataset", dataset="/StreamExpress/Run2018A-Express-v1/DQMIO"
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend(
            "oms.OmsRun",
            run_number=300100,
            run_type="collisions",
            stable_beam=True,
            hlt_key="/cdaq/physics",
            b_field="3.8",
            energy="13",
            fill_type_party1="Proton-Proton",
        ),
        reconstruction="express",
        dataset=dataset1,
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=False,
        run=mixer.blend(
            "oms.OmsRun",
            run_number=300101,
            run_type="collisions",
            stable_beam=True,
            hlt_key="/cdaq/physics",
            b_field="3.8",
            energy="13",
            fill_type_party1="Proton-Proton",
        ),
        reconstruction="express",
        dataset=dataset1,
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend(
            "oms.OmsRun",
            run_number=300150,
            run_type="collisions",
            stable_beam=True,
            hlt_key="/cdaq/physics",
            b_field="3.8",
            energy="13",
            fill_type_party1="Proton-Proton",
        ),
        reconstruction="prompt",
        dataset=mixer.blend(
            "certifier.Dataset", dataset="/ZeroBias/Run2018D-PromptReco-v2/DQMIO"
        ),
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend(
            "oms.OmsRun",
            run_number=300200,
            run_type="cosmics",
            b_field="3.8",
            energy="0",
            fill_type_party1="Cosmics",
        ),
        reconstruction="express",
        dataset=mixer.blend(
            "certifier.Dataset",
            dataset="/StreamExpressCosmics/Run2018D-Express-v1/DQMIO",
        ),
    )

    mixer.blend(
        "certifier.RunReconstruction",
        is_reference=True,
        run=mixer.blend(
            "oms.OmsRun",
            run_number=300250,
            run_type="cosmics",
            b_field="3.8",
            energy="0",
            fill_type_party1="Cosmics",
        ),
        reconstruction="prompt",
        dataset=mixer.blend(
            "certifier.Dataset", dataset="/Cosmics/Run2018D-PromptReco-v2/DQMIO"
        ),
    )


@pytest.fixture
def runs_for_summary_report(legitimate_reference_runs):
    """
    Certified runs for the current day.
    Used to test the summary report.

    All runs will be assigned to the first User that exists.

    Code was partially generated via print_mixer_code() helper in utilities.py
    """

    ref_runs = RunReconstruction.objects.all()
    r1 = ref_runs.filter(
        run__run_type="collisions", reconstruction="express", is_reference=True
    )[0]
    r2 = ref_runs.filter(
        run__run_type="collisions", reconstruction="prompt", is_reference=True
    )[0]
    r3 = ref_runs.filter(
        run__run_type="cosmics", reconstruction="express", is_reference=True
    )[0]
    r4 = ref_runs.filter(
        run__run_type="cosmics", reconstruction="prompt", is_reference=True
    )[0]

    today = timezone.now().date

    user = get_user_model().objects.first()

    dataset1 = Dataset.objects.get(dataset="/Cosmics/Run2018D-PromptReco-v2/DQMIO")
    dataset2 = Dataset.objects.get(
        dataset="/StreamExpressCosmics/Run2018D-Express-v1/DQMIO"
    )
    dataset3 = Dataset.objects.get(dataset="/ZeroBias/Run2018D-PromptReco-v2/DQMIO")
    dataset4 = Dataset.objects.get(dataset="/StreamExpress/Run2018A-Express-v1/DQMIO")

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300024,
                lumisections="372",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r4,
        trackermap="missing",
        pixel_lowstat=True,
        strip_lowstat=True,
        tracking="excluded",
        date=today,
        comment="""Water specific forget carry week. Likely 
                friend claim marriage. White long design. Drop daughter free free 
                analysis hang what run. Hospital administration one while the call.""",
        dataset=dataset1,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300023,
                lumisections="207",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r3,
        trackermap="exists",
        pixel="good",
        strip="good",
        tracking="bad",
        date=today,
        comment="""Her arrive course management training probably anyone.
    Thank cut right manage enough state lose.""",
        dataset=dataset2,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300022,
                lumisections="74",
                recorded_lumi="874.62",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="missing",
        pixel="excluded",
        strip="excluded",
        tracking_lowstat=True,
        date=today,
        comment="""After weight institution whose produce. End 
                away finish anything voice. Turn worker success rather argue. Animal 
                right music material. Development clear suddenly bank send central 
                wall.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300021,
                lumisections="367",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r3,
        trackermap="missing",
        pixel="good",
        strip="bad",
        tracking="excluded",
        date=today,
        comment="""Still a usually member quite many cause. Summer now finish 
                may anything. Best hang light spend happen. Accept idea if should 
                possible ball official.""",
        dataset=dataset2,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300020,
                lumisections="793",
                recorded_lumi="572.98",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="exists",
        pixel="excluded",
        strip_lowstat=True,
        tracking="bad",
        date=today,
        comment="""Part by fight such policy candidate cold. Happy career 
                hope who. 

                Apply around seem win dog. Walk shot far record decade 
                message trouble.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300019,
                lumisections="520",
                recorded_lumi="433.99",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="missing",
        pixel="excluded",
        strip="good",
        tracking="excluded",
        date=today,
        comment="""Nor particular them win share fire agree. Job kind offer 
                war lawyer couple card. Young degree go thus whether including away 
                on.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300018,
                lumisections="242",
                recorded_lumi="983.49",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r1,
        trackermap="exists",
        pixel="excluded",
        strip_lowstat=True,
        tracking="bad",
        date=today,
        comment="""Attack strategy raise smile and. West but alone position 
                ago finish change. Another message computer blood provide else 
                hard.""",
        dataset=dataset4,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300017,
                lumisections="142",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r4,
        trackermap="missing",
        pixel="excluded",
        strip="good",
        tracking="bad",
        date=today,
        comment="""Employee hard hard cost near enter recent. Remember plan 
                hang.""",
        dataset=dataset1,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300016,
                lumisections="188",
                recorded_lumi="391.13",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="exists",
        pixel="excluded",
        strip="good",
        tracking="bad",
        date=today,
        comment="""Why before work contain these indicate seem. None clear 
                pass near minute once. Surface floor focus car number high still. 
                Western trial collection evidence prepare.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300015,
                lumisections="265",
                recorded_lumi="432.73",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="missing",
        pixel_lowstat=True,
        strip_lowstat=True,
        tracking_lowstat=True,
        date=today,
        comment="""Better private while allow example style. Activity along 
                me effort. Exactly thing commercial hang. Course shake red son source 
                anything.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300014,
                lumisections="164",
                recorded_lumi="836.49",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="exists",
        pixel="excluded",
        strip="good",
        tracking="excluded",
        date=today,
        comment="""Might surface line shoulder fund institution. 
                Factor pretty or sign benefit ten. Stock study nation bill. Use image 
                kitchen establish explain eye north still. Anyone news fight huge 
                region.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300013,
                lumisections="642",
                recorded_lumi="138.83",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="missing",
        pixel="good",
        strip_lowstat=True,
        tracking="excluded",
        date=today,
        comment="""Bill suggest success new citizen. Clear apply already rich 
                cultural mouth support. Parent their case some win your news. Garden 
                wear body into character. Age security including later involve.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300012,
                lumisections="365",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r4,
        trackermap="exists",
        pixel="bad",
        strip="bad",
        tracking="bad",
        date=today,
        comment="""Care agree might TV paper response. Future support 
                certainly follow thousand network. Positive cell raise no property 
                science. Economic suffer market trade politics region huge.""",
        dataset=dataset1,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300011,
                lumisections="826",
                recorded_lumi="621.59",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r1,
        trackermap="missing",
        pixel="excluded",
        strip_lowstat=True,
        tracking="bad",
        date=today,
        comment="""Serious character against water. With customer product 
                different. Understand heart civil main sit. Best set baby. 
                Traditional person picture create love maybe. Another his compare 
                gas.""",
        dataset=dataset4,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300010,
                lumisections="378",
                recorded_lumi="786.43",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r1,
        trackermap="missing",
        pixel="excluded",
        strip="bad",
        tracking="excluded",
        date=today,
        comment="""Contain many the into television. Finally age little 
                treat. Note PM mention how oh assume wrong. Inside listen health. Off 
                degree how economy scientist.""",
        dataset=dataset4,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300009,
                lumisections="134",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r3,
        trackermap="exists",
        pixel_lowstat=True,
        strip="good",
        tracking_lowstat=True,
        date=today,
        comment="""Turn drug science practice. Drop four budget section. Into 
                draw more rock create pretty democratic. Really clear determine 
                agreement foreign already him.""",
        dataset=dataset2,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300008,
                lumisections="356",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r4,
        trackermap="missing",
        pixel_lowstat=True,
        strip="bad",
        tracking="good",
        date=today,
        comment="""Try billion collection lose. Site near thank class yard 
                major. Test anyone much either exactly candidate east. Hit force oh 
                professional network wide during fear. Pick figure young 
                television.""",
        dataset=dataset1,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300007,
                lumisections="341",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r4,
        trackermap="missing",
        pixel_lowstat=True,
        strip_lowstat=True,
        tracking_lowstat=True,
        date=today,
        comment="""Yard central myself leg sit. Consumer remember fund 
                control then. Even near see girl hit season.""",
        dataset=dataset1,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300006,
                lumisections="399",
                recorded_lumi="954.85",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="missing",
        pixel="excluded",
        strip="excluded",
        tracking="bad",
        date=today,
        comment="""Training adult impact treatment die military. Glass cost 
                experience various rather anything human. Either gas area may and 
                any.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300005,
                lumisections="981",
                recorded_lumi="510.75",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r1,
        trackermap="exists",
        pixel="good",
        strip="excluded",
        tracking="bad",
        date=today,
        comment="""Enter quality material once rule with bill wind. Far whole 
                give run. Government authority many wish sport.""",
        dataset=dataset4,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300004,
                lumisections="441",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r3,
        trackermap="missing",
        pixel="excluded",
        strip="bad",
        tracking="bad",
        date=today,
        comment="""Notice in affect information value carry. Great success 
                which on. Nation join doctor event. Actually local economy positive. 
                Left woman effort technology reality. Military you it.""",
        dataset=dataset2,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300003,
                lumisections="574",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r3,
        trackermap="missing",
        pixel_lowstat=True,
        strip_lowstat=True,
        tracking="good",
        date=today,
        comment="""Ball west movie pain enough. Child tonight guy hotel 
                knowledge. Of everything past language heavy general. Goal option 
                probably prevent. Wonder general difference design test.""",
        dataset=dataset2,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300002,
                lumisections="873",
                recorded_lumi="273.88",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="exists",
        pixel="good",
        strip="excluded",
        tracking="bad",
        date=today,
        comment="""Important front more because nation check. Shoot accept 
                seem detail stand under. Poor shoot next admit close conference. Put 
                research watch mind.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300025,
                lumisections="834",
                recorded_lumi="840.18",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r2,
        trackermap="exists",
        pixel="good",
        strip="excluded",
        tracking_lowstat=True,
        date=today,
        comment="""Vote kind rule loss dark course. Across difficult people shoot.
    Thought real yeah improve. Explain media book yes business east.""",
        dataset=dataset3,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300001,
                lumisections="997",
                recorded_lumi="632.57",
                run_type="collisions",
                stable_beam=True,
                hlt_key="/cdaq/physics",
                b_field="3.8",
                energy="13",
                fill_type_party1="Proton-Proton",
            ),
            reconstruction="express",
        ),
        reference_runreconstruction=r1,
        trackermap="exists",
        pixel="bad",
        strip="excluded",
        tracking="excluded",
        date=today,
        comment="""Develop should across truth prevent single. Thus this much 
                method child. Population impact accept black drop say. Game thought 
                senior.""",
        dataset=dataset4,
    )

    mixer.blend(
        "certifier.TrackerCertification",
        user=user,
        runreconstruction=mixer.blend(
            "certifier.RunReconstruction",
            run=mixer.blend(
                "oms.OmsRun",
                run_number=300000,
                lumisections="856",
                recorded_lumi="0.00",
                run_type="cosmics",
                b_field="3.8",
                energy="0",
                fill_type_party1="Cosmics",
            ),
            reconstruction="prompt",
        ),
        reference_runreconstruction=r4,
        trackermap="exists",
        pixel="good",
        strip_lowstat=True,
        tracking="bad",
        date=today,
        comment="""Notice this resource center. Interest remain throughout 
                condition contain save problem. Town treatment magazine environmental 
                report all rule.""",
        dataset=dataset1,
    )
