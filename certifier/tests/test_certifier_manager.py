from decimal import Decimal

import math
import pytest
from mixer.backend.django import mixer

from certifier.models import TrackerCertification
from summary.utilities.utilities import get_from_summary

pytestmark = pytest.mark.django_db
from oms.models import OmsRun

class TestTrackerCertificationManager:
    def test_good(self):
        run = mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="cosmics")),
            strip="bad",
        )
        assert run.is_good is False

        run = mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="cosmics")),
            strip="good",
            tracking="bad",
        )
        assert run.is_good is False

        run = mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="cosmics")),
            strip="good",
            tracking="good",
        )
        assert run.is_good is True

        run = mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
            strip="bad",
        )
        assert run.is_good is False

        run = mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
            pixel="bad",
            pixel_lowstat=False,
        )
        assert run.is_good is False

        run = mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
            tracking="bad",
        )
        assert run.is_good is False

        run = mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun",stable_beam=True, hlt_key="/cdaq/physics", run_type="collisions")),
            pixel="good",
            strip="good",
            tracking="good",
        )
        assert run.is_good is True

        assert len(TrackerCertification.objects.all()) == 7
        good_runs = TrackerCertification.objects.all().good().order_by("pk")
        assert len(good_runs) == 2
        assert good_runs[0].runreconstruction.run.run_type == "cosmics"
        assert good_runs[0].strip == "good"
        assert good_runs[0].tracking == "good"
        assert good_runs[1].runreconstruction.run.run_type == "collisions"
        assert good_runs[1].strip == "good"
        assert good_runs[1].pixel == "good"
        assert good_runs[1].tracking == "good"

        bad_runs = TrackerCertification.objects.all().bad().order_by("pk")

        assert len(bad_runs) == 5

        assert len(TrackerCertification.objects.bad()) == 5
        assert len(TrackerCertification.objects.good()) == 2

    def test_summary(self):
        conditions = [
            ["cosmics", "express", 0.1234, 72, "dsadas",19],
            ["collisions", "prompt", 1.234, 5432, "/cdaq/physics",18],
            ["cosmics", "prompt", 0, 25,"dsdas",17],
            ["collisions", "express", 423.24, 2, "/cdaq/physics",1],
            ["collisions", "express", 0, 72, "/cdaq/physics",2],
            ["cosmics", "express", 0, 12, "dasdasd",3],
            ["cosmics", "express", 0, 72, "sdsadasd",4],
            ["cosmics", "express", 0, 42, "dsadasd",5],
            ["collisions", "express", 124.123, 72, "/cdaq/physics",6],
            ["cosmics", "express", 0, 1242, "dsdas",7],
            ["cosmics", "express", 0, 72, "sdsadas",8],
            ["collisions", "express", 999, 142,"/cdaq/physics",9],
            ["collisions", "prompt", 0, 72, "/cdaq/physics",10],
            ["collisions", "prompt", 123132.32, 4522, "/cdaq/physics",11],
            ["collisions", "express", 0, 72, "/cdaq/physics",12],
            ["collisions", "express", -1, 71232, "/cdaq/physics",13],
            ["cosmics", "express", 0, 712, "sdsdsadas",14],
            ["collisions", "express", 5213, 142, "/cdaq/physics",15],
            ["collisions", "express", 154543, 72, "/cdaq/physics",16],
        ]

        runs = []

        for condition in conditions:
            runs.append(
                mixer.blend(
                    "certifier.TrackerCertification",
                    runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=condition[1], run=mixer.blend(OmsRun,run_number=condition[5], run_type=condition[0], recorded_lumi=condition[2], lumisections=condition[3], hlt_key=condition[4], stable_beam=True))
                )
            )

        summary = TrackerCertification.objects.all().summary()

        a = [
            x
            for x in summary
            if x["runreconstruction__run__run_type"] == "collisions" and x["runreconstruction__reconstruction"] == "express"
        ]

        assert len(a) == 1
        a = a[0]
        assert a["runs_certified"] == 8
        assert math.isclose(161301.363, a["int_luminosity"], abs_tol=0.1)
        assert a["number_of_ls"] == 71806

        a = get_from_summary(summary, "cosmics", "express")

        assert len(a) == 1
        a = a[0]
        assert a["runs_certified"] == 7
        assert a["int_luminosity"] == 0.1234
        assert a["number_of_ls"] == 2224

        a = [
            x
            for x in summary
            if x["runreconstruction__run__run_type"] == "collisions" and x["runreconstruction__reconstruction"] == "prompt"
        ]

        assert len(a) == 1
        a = a[0]
        assert a["runs_certified"] == 3
        assert a["int_luminosity"] == 123133.554
        assert a["number_of_ls"] == 10026

        a = [
            x
            for x in summary
            if x["runreconstruction__run__run_type"] == "cosmics" and x["runreconstruction__reconstruction"] == "prompt"
        ]

        assert len(a) == 1
        a = a[0]
        assert a["runs_certified"] == 1
        assert a["int_luminosity"] == 0
        assert a["number_of_ls"] == 25

        a = get_from_summary(summary, "cosmics", "prompt")
        assert len(a) == 1
        a = a[0]
        assert a["runs_certified"] == 1
        assert a["int_luminosity"] == 0
        assert a["number_of_ls"] == 25

    def test_summary_per_day(self):
        conditions = [
            ["cosmics", "express", 0.1234, 72, "2018-05-14", "nothing"],
            ["collisions", "prompt", 1.234, 5432, "2018-05-14", "/cdaq/physics"],
            ["cosmics", "prompt", 0, 25, "2018-05-14", "nothing"],
            ["collisions", "express", 423.24, 2, "2018-05-15", "/cdaq/physics"],
            ["collisions", "express", 0, 72, "2018-05-14", "/cdaq/physics"],
            ["cosmics", "express", 0, 12, "2018-05-17", "nothing"],
            ["cosmics", "express", 0, 72, "2018-05-17", "nothing"],
            ["cosmics", "express", 0, 42, "2018-05-14", "nothing"],
            ["collisions", "express", 124.123, 72, "2018-05-18", "/cdaq/physics"],
            ["cosmics", "express", 0, 1242, "2018-05-14", "nothing"],
            ["cosmics", "express", 0, 72, "2018-05-20", "nothing"],
            ["collisions", "express", 999, 142, "2018-05-20", "/cdaq/physics"],
            ["collisions", "prompt", 0, 72, "2018-05-20", "/cdaq/physics"],
            ["collisions", "prompt", 123132.32, 4522, "2018-05-20", "/cdaq/physics"],
            ["collisions", "express", 0, 72, "2018-05-20", "/cdaq/physics"],
            ["collisions", "express", -1, 71232, "2018-05-14", "/cdaq/physics"],
            ["cosmics", "express", 0, 712, "2018-05-17", "nothing"],
            ["collisions", "express", 5213, 142, "2018-05-14", "/cdaq/physics"],
            ["collisions", "express", 154543, 72, "2018-05-18", "/cdaq/physics"],
        ]

        runs = []

        for condition in conditions:
            runs.append(
                mixer.blend(
                    "certifier.TrackerCertification",
                    runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=condition[1], run=mixer.blend(OmsRun, run_type=condition[0], recorded_lumi=condition[2], lumisections=condition[3], hlt_key=condition[5], stable_beam=True)),
                    date=condition[4],
                )
            )

        summary = TrackerCertification.objects.all().summary_per_day()

        assert len(summary) == 10

        item = get_from_summary(summary, "collisions", "prompt", "2018-05-14")

        assert len(item) == 1

        assert len(get_from_summary(summary, date="2018-05-14")) == 4
        assert (
            len(get_from_summary(summary, runtype="collisions", date="2018-05-14")) == 2
        )
        assert len(get_from_summary(summary, reco="express", date="2018-05-14")) == 2
        assert (
            len(get_from_summary(summary, "collisions", "express", "2018-05-14")) == 1
        )
        assert len(get_from_summary(summary, date="2018-05-15")) == 1
        assert len(get_from_summary(summary, date="2018-05-16")) == 0
        assert len(get_from_summary(summary, date="2018-05-17")) == 1
        assert len(get_from_summary(summary, date="2018-05-18")) == 1
        assert len(get_from_summary(summary, date="2018-05-19")) == 0
        assert len(get_from_summary(summary, date="2018-05-20")) == 3

        assert (
           154667.123 == get_from_summary(summary, date="2018-05-18")[0]["int_luminosity"]
        )
        assert get_from_summary(summary, date="2018-05-18")[0]["number_of_ls"] == 144
        assert get_from_summary(summary, date="2018-05-14")[2]["int_luminosity"] == 0.1234

    def test_check_if_certified(self, some_certified_runs):
        check = TrackerCertification.objects.check_if_certified(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]
        )

        assert check["missing"] == [0, 8, 15]

        collisions = check["collisions"]
        cosmics = check["cosmics"]

        assert collisions["good"] == [1, 3]
        assert collisions["bad"] == [6]
        assert collisions["prompt_missing"] == [2, 7]
        assert collisions["changed_good"] == [5]
        assert collisions["changed_bad"] == [4]

        assert cosmics["good"] == [11]
        assert cosmics["bad"] == []
        assert cosmics["prompt_missing"] == [10, 12, 13]
        assert cosmics["changed_good"] == []
        assert cosmics["changed_bad"] == [14]

        check = TrackerCertification.objects.check_if_certified(
            [
                0,
                "1",
                "2",
                3,
                "4",
                5,
                "6",
                "hase",
                "7",
                8,
                "10",
                11,
                "12",
                "13",
                "14",
                "15",
                "abc",
            ]
        )

        collisions = check["collisions"]
        cosmics = check["cosmics"]

        assert collisions["good"] == [1, 3]
        assert collisions["bad"] == [6]
        assert collisions["prompt_missing"] == [2, 7]
        assert collisions["changed_good"] == [5]
        assert collisions["changed_bad"] == [4]

        assert cosmics["good"] == [11]
        assert cosmics["bad"] == []
        assert cosmics["prompt_missing"] == [10, 12, 13]
        assert cosmics["changed_good"] == []
        assert cosmics["changed_bad"] == [14]

    def test_check_integrity_of_run(self):
        """
        Checks if the given run has any inconsistencies with already certified runs.
        :return:
        """

        runreconstruction_express=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=111111, recorded_lumi="8071403146.0", lumisections="1550390125", fill_type_party1="HeavyIon-Proton"), reconstruction="express")
        runreconstruction_prompt=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=111111, recorded_lumi="8071403146.0", lumisections="1550390125", fill_type_party1=runreconstruction_express.run.fill_type_party1, run_type=runreconstruction_express.run.run_type, b_field=runreconstruction_express.run.b_field, run_energy=runreconstruction_express.run.energy), reconstruction="prompt")

        runreconstruction_express_ref=mixer.blend("certifier.RunReconstruction", reconstruction="express", is_reference=True)
        runreconstruction_prompt_ref=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", is_reference=True)

        express_run = mixer.blend("certifier.TrackerCertification", runreconstruction=runreconstruction_express, reference_runreconstruction=runreconstruction_express_ref)

        prompt_run = TrackerCertification.objects.get()
        prompt_run.runreconstruction = runreconstruction_prompt
        prompt_run.reference_runreconstruction = runreconstruction_prompt_ref

        assert {} == TrackerCertification.objects.check_integrity_of_run(prompt_run)

        prompt_run.runreconstruction.run.fill_type_party1 = "Proton-Proton"

        assert "fill_type_party1" in TrackerCertification.objects.check_integrity_of_run(prompt_run)

        prompt_run.save()
        assert express_run.pk + 1 == prompt_run.pk

        assert "fill_type_party1" in TrackerCertification.objects.check_integrity_of_run(prompt_run)

        express_run.pixel = "good"
        express_run.save()
        prompt_run.pixel = "lowstat"
        assert "fill_type_party1" in TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert "pixel" in TrackerCertification.objects.check_integrity_of_run(prompt_run)

        prompt_run.runreconstruction.run.fill_type_party1 = "HeavyIon-Proton"
        express_run.pixel = "lowstat"
        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert "pixel" in check
        assert "good" == check["pixel"]
        assert "good" != prompt_run.pixel
        express_run.save()
        prompt_run.save()

        assert {} == TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {} == TrackerCertification.objects.check_integrity_of_run(express_run)

        express_run.runreconstruction.run.run_type = "cosmics"
        prompt_run.runreconstruction.run.run_type = "collisions"
        express_run.runreconstruction.run.save()

        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {"run_type": "cosmics"} == check
        prompt_run.runreconstruction.run.run_type = "cosmics"

        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {} == check

        express_run.runreconstruction.run.recorded_lumi = 3.1
        prompt_run.runreconstruction.run.recorded_lumi = 3.3
        express_run.runreconstruction.run.save()

        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {"recorded_lumi": 3.1} == check

        prompt_run.runreconstruction.run.recorded_lumi = 3.2
        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {} == check

        prompt_run.runreconstruction.reconstruction = "rereco"
        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {} == check

        prompt_run.runreconstruction = mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=121322), reconstruction="express")
        prompt_run.runreconstruction.save()
        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {} == check

        prompt_run.runreconstruction = None
        check = TrackerCertification.objects.check_integrity_of_run(prompt_run)
        assert {} == check
