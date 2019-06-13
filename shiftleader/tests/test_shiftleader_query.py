import math
import pytest
from mixer.backend.django import mixer

from oms.models import OmsRun
from certifier.models import TrackerCertification, RunReconstruction
from shiftleader.utilities.utilities import to_date, to_weekdayname
from certifier.utilities.utilities import uniquely_sorted
from utilities.utilities import create_runs
from utilities.credentials import SHIFTER1_USERNAME

pytestmark = pytest.mark.django_db

class TestTrackerCertificationQuerySet:
    def test_fill_numbers_empty(self):
        runs = TrackerCertification.objects.all()
        assert [] == runs.fill_numbers()

    def test_lumisections_empty(self):
        runs = TrackerCertification.objects.all()
        assert 0 == runs.lumisections()

    def test_compare_list_if_certified(self):
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=1234, run_type="cosmics"), reconstruction="express"),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=8765, run_type="cosmics")),
            pixel="good",
            strip="good",
            tracking="bad",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=4321, run_type="cosmics"), reconstruction="express"),
            pixel="good",
            strip="good",
            tracking="bad",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=6543)),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=6655, run_type="cosmics")),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=9876)),
            pixel="good",
            strip="good",
            tracking="bad",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=444, run_type="cosmics"), reconstruction="express"),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=444, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True), reconstruction="prompt"),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=333, run_type="cosmics"), reconstruction="express"),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=333, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True), reconstruction="prompt"),
            pixel="good",
            strip="good",
            tracking="bad",
        )
        mixer.blend(
            "certifier.TrackerCertification", 
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=999)),
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=800, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=4321, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True), reconstruction="prompt"),
            pixel="good",
            strip="good",
            tracking="good",
        )
        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=1234, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True), reconstruction="prompt"),
            pixel="good",
            strip="good",
            tracking="good",
        )

        d = TrackerCertification.objects.all().compare_list_if_certified(
            [333, 1234, 6655, "800", 4321, 7777, 9876, "abde", 8765, 6543, 888, 444]
        )

        assert set([1234, 6655, 6543, 444, "800"]) == set(d["good"])
        assert set([9876, 8765]) == set(d["bad"])
        assert set([7777, 888, "abde"]) == set(d["missing"])
        assert set([4321, 333]) == set(d["different_flags"])

    def test_changed_flags(self, some_certified_runs):
        """
        run     type       reco    good
        1       Collisions Express True
        1       Collisions Prompt  True
        2       Collisions Express True
        3       Collisions Express True
        3       Collisions Prompt  True
        4       Collisions Express True
        4       Collisions Prompt  False
        5       Collisions Express False
        5       Collisions Prompt  True
        6       Collisions Express False
        6       Collisions Prompt  False
        7       Collisions Express False
        10      Cosmics    Express True
        11      Cosmics    Express True
        11      Cosmics    Prompt  True
        12      Cosmics    Express True
        13      Cosmics    Express True
        14      Cosmics    Express True
        14      Cosmics    Prompt  False
        """
        assert 3 == len(TrackerCertification.objects.all().changed_flags())
        assert {5, 4, 14} == set(TrackerCertification.objects.all().changed_flags())

    def test_no_changed_flags(self):
        assert 0 == len(TrackerCertification.objects.all().changed_flags())

    def test_filter_flag_changed(self, some_certified_runs):
        runs = TrackerCertification.objects.all()
        runs_flag_changed = runs.filter_flag_changed()
        run_numbers = uniquely_sorted(runs_flag_changed.run_numbers())
        assert [4, 5, 14] == run_numbers
        assert True

    def test_collisions(self, some_certified_runs):
        assert 0 != len(TrackerCertification.objects.all())
        runs = TrackerCertification.objects.all().collisions()
        assert 0 != len(runs)

        for run in runs:
            assert "collisions" == run.runreconstruction.run.run_type

    def test_collisions_prompt(self):
        create_runs(5, 1, "collisions", "express")
        create_runs(3, 5, "collisions", "prompt")
        create_runs(5, 20, "cosmics", "express")
        create_runs(4, 26, "cosmics", "express")

        runs = TrackerCertification.objects.all().collisions()
        assert 8 == len(runs)

        for run in runs:
            assert "collisions" == run.runreconstruction.run.run_type

        runs = TrackerCertification.objects.all().collisions().prompt()
        assert 3 == len(runs)

        runs = TrackerCertification.objects.all().collisions().express()
        assert 5 == len(runs)

    def test_collisions_prompt_bad(self):
        create_runs(5, 1, "collisions", "express", good=True)
        create_runs(4, 6, "collisions", "express", good=False)
        create_runs(3, 10, "collisions", "prompt", good=True)
        create_runs(3, 15, "collisions", "prompt", good=False)
        create_runs(5, 21, "cosmics", "express", good=True)
        create_runs(4, 26, "cosmics", "express", good=False)
        create_runs(3, 30, "cosmics", "prompt", good=True)
        create_runs(3, 35, "cosmics", "prompt", good=False)

        runs = TrackerCertification.objects.all().collisions().prompt()
        assert 6 == len(runs)

    def test_cosmics(self, some_certified_runs):
        runs = TrackerCertification.objects.all().cosmics()
        assert 0 != len(runs)

        for run in runs:
            assert "cosmics" == run.runreconstruction.run.run_type

    def test_express(self, some_certified_runs):
        runs = TrackerCertification.objects.all().express()
        assert 0 != len(runs)

        for run in runs:
            assert "express" == run.runreconstruction.reconstruction

    def test_prompt(self, some_certified_runs):
        runs = TrackerCertification.objects.all().prompt()
        assert 0 != len(runs)

        for run in runs:
            assert "prompt" == run.runreconstruction.reconstruction

    def test_rereco(self, some_certified_runs):
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction",reconstruction="rereco"))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction",reconstruction="rereco"))
        runs = TrackerCertification.objects.all().rereco()
        assert 0 != len(runs)

        for run in runs:
            assert "rereco" == run.runreconstruction.reconstruction

    def test_run_numbers(self):
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=123456)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="express", run=mixer.blend("oms.OmsRun", run_number=234567)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction="prompt", run=mixer.blend("oms.OmsRun", run_number=234567)))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=345678)))

        assert [123456, 234567, 234567, 345678] == TrackerCertification.objects.all().run_numbers()

    def test_pks(self):
        a = mixer.blend("certifier.TrackerCertification").pk
        b = mixer.blend("certifier.TrackerCertification").pk
        c = mixer.blend("certifier.TrackerCertification").pk

        assert [a, b, c] == TrackerCertification.objects.all().pks()

    def test_int_luminosity(self):
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", recorded_lumi="13")))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", recorded_lumi="12.2")))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", recorded_lumi="0")))
        mixer.blend("certifier.TrackerCertification", runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", recorded_lumi="9")))
        assert 34.2 == TrackerCertification.objects.all().integrated_luminosity()

    def test_total_number(self, some_certified_runs):
        assert 19 == TrackerCertification.objects.all().total_number()
        assert len(TrackerCertification.objects.all()) == TrackerCertification.objects.all().total_number()

    def test_slr(self, runs_for_slr):
        runs = TrackerCertification.objects.all()

        collisions_express = runs.collisions().express()
        collisions_prompt = runs.collisions().prompt()
        cosmics_express = runs.cosmics().express()
        cosmics_prompt = runs.cosmics().prompt()

        assert collisions_express.total_number() == 8
        assert collisions_prompt.total_number() == 3
        assert cosmics_express.total_number() == 7
        assert cosmics_prompt.total_number() == 1

        assert math.isclose(161301.363, collisions_express.integrated_luminosity(), abs_tol=0.1)
        assert collisions_prompt.integrated_luminosity() == 123133.554
        assert cosmics_express.integrated_luminosity() == 0.1234
        assert cosmics_prompt.integrated_luminosity() == 0

        assert collisions_express.bad().total_number() == 0
        assert collisions_prompt.bad().total_number() == 3
        assert cosmics_express.bad().total_number() == 2
        assert cosmics_prompt.bad().total_number() == 1

        assert collisions_express.bad().integrated_luminosity() == 0
        assert collisions_prompt.bad().integrated_luminosity() == 123133.554
        assert cosmics_express.bad().integrated_luminosity() == 0
        assert cosmics_prompt.bad().integrated_luminosity() == 0

    def test_days(self, runs_for_slr):
        days = TrackerCertification.objects.all().days()
        assert 5 == len(days)
        assert "2018-05-14" == days[0]
        assert "2018-05-15" == days[1]
        assert "2018-05-17" == days[2]
        assert "2018-05-18" == days[3]
        assert "2018-05-20" == days[4]

    def test_slr_per_day(self, runs_for_slr):
        runs = TrackerCertification.objects.all()
        days = runs.days()

        runs = runs.filter(date=days[0])

        collisions_express = runs.collisions().express()
        collisions_prompt = runs.collisions().prompt()
        cosmics_express = runs.cosmics().express()
        cosmics_prompt = runs.cosmics().prompt()

        assert collisions_express.total_number() == 3
        assert collisions_prompt.total_number() == 1
        assert cosmics_express.total_number() == 3
        assert cosmics_prompt.total_number() == 1

        assert collisions_express.integrated_luminosity() == 5212
        assert 1.234 == collisions_prompt.integrated_luminosity()
        assert cosmics_express.integrated_luminosity() == 0.1234
        assert cosmics_prompt.integrated_luminosity() == 0

        assert collisions_express.bad().total_number() == 0
        assert collisions_prompt.bad().total_number() == 1
        assert cosmics_express.bad().total_number() == 1
        assert cosmics_prompt.bad().total_number() == 1

        assert collisions_express.bad().integrated_luminosity() == 0
        assert collisions_prompt.bad().integrated_luminosity() == 1.234
        assert cosmics_express.bad().integrated_luminosity() == 0
        assert cosmics_prompt.bad().integrated_luminosity() == 0

        assert to_weekdayname(days[0]) == "Monday"
        assert to_weekdayname(days[3]) == "Friday"
        assert to_weekdayname(days[4]) == "Sunday"

    def test_reference_run_ids(self, runs_with_three_refs):
        refs = TrackerCertification.objects.all().reference_run_numbers()
        assert 3 == len(refs)
        assert 1 == refs[0]
        assert 2 == refs[1]
        assert 3 == refs[2]

    def test_reference_runs(self, runs_with_three_refs):
        refs = TrackerCertification.objects.all().reference_runs().order_by("run__run_number")
        assert 3 == len(refs)
        assert RunReconstruction.objects.get(run__run_number=1) == refs[0]
        assert RunReconstruction.objects.get(run__run_number=2) == refs[1]
        assert RunReconstruction.objects.get(run__run_number=3) == refs[2]

    def test_runs(self, runs_with_three_refs):
        refs = TrackerCertification.objects.all().runs().order_by("run__run_number")
        assert 3 == len(refs)
        assert RunReconstruction.objects.get(run__run_number=1) == refs[0]
        assert RunReconstruction.objects.get(run__run_number=2) == refs[1]
        assert RunReconstruction.objects.get(run__run_number=3) == refs[2]

    def test_types(self):
        t1 = runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True))
        t2 = runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_type="cosmics"))

        r1 = mixer.blend("certifier.TrackerCertification", runreconstruction=t2)
        r2 = mixer.blend("certifier.TrackerCertification", runreconstruction=t2)
        r3 = mixer.blend("certifier.TrackerCertification", runreconstruction=t2)
        r4 = mixer.blend("certifier.TrackerCertification", runreconstruction=t2)
        r5 = mixer.blend("certifier.TrackerCertification", runreconstruction=t1)
        r6 = mixer.blend("certifier.TrackerCertification", runreconstruction=t2)
        r7 = mixer.blend("certifier.TrackerCertification", runreconstruction=t1)
        r8 = mixer.blend("certifier.TrackerCertification", runreconstruction=t2)
        r9 = mixer.blend("certifier.TrackerCertification", runreconstruction=t1)
        r10 = mixer.blend("certifier.TrackerCertification", runreconstruction=t2)

        runs = TrackerCertification.objects.all()
        types = runs.types()
        assert 2 == len(types)
        assert t1.run.run_type in str(types)
        assert t2.run.run_type in str(types)

        per_type = runs.per_type()
        assert r5 in per_type[0]
        assert r9 in per_type[0]
        assert t1.run.run_type == per_type[0][0].runreconstruction.run.run_type

        assert r1 in per_type[1]
        assert r2 in per_type[1]
        assert r3 in per_type[1]
        assert r4 in per_type[1]
        assert r6 in per_type[1]
        assert r8 in per_type[1]
        assert r10 in per_type[1]
        assert t2.run.run_type == per_type[1][0].runreconstruction.run.run_type
        assert r7 in per_type[0]
        assert t1.run.run_type == per_type[0][0].runreconstruction.run.run_type

    def test_per_day(self, runs_for_slr):
        runs = TrackerCertification.objects.all().per_day()
        assert 5 == len(runs)

        for run in runs[0]:
            assert to_date("2018-05-14") == run.date
            assert "Monday" == to_weekdayname(run.date)

        for run in runs[1]:
            assert to_date("2018-05-15") == run.date
            assert "Tuesday" == to_weekdayname(run.date)

        for run in runs[2]:
            assert to_date("2018-05-17") == run.date
            assert "Thursday" == to_weekdayname(run.date)

        for run in runs[3]:
            assert to_date("2018-05-18") == run.date
            assert "Friday" == to_weekdayname(run.date)

        for run in runs[4]:
            assert to_date("2018-05-20") == run.date
            assert "Sunday" == to_weekdayname(run.date)

    def test_trackermap_missing(self):
        mixer.blend("certifier.TrackerCertification", trackermap="Exists")
        mixer.blend("certifier.TrackerCertification", trackermap="Exists")
        mixer.blend("certifier.TrackerCertification", trackermap="Missing")
        mixer.blend("certifier.TrackerCertification", trackermap="Exists")
        mixer.blend("certifier.TrackerCertification", trackermap="Exists")
        mixer.blend("certifier.TrackerCertification", trackermap="Missing")

        runs = TrackerCertification.objects.all()

        assert len(runs)
        assert len(runs.trackermap_missing()) == 2

    def test_print_verbose(self, shifter, runs_for_summary_report):
        print()
        for t in RunReconstruction.objects.filter(is_reference=True):
            print(t)
        TrackerCertification.objects.all().order_by("runreconstruction__run__run_number").print_verbose()
        TrackerCertification.objects.all().order_by("runreconstruction__run__run_number").print_reference_runs()
        TrackerCertification.objects.all().order_by("runreconstruction__run__run_number").print_runs()
        TrackerCertification.objects.all().order_by("runreconstruction__run__run_number").print()

    def test_shifters(self, shifter, runs_for_summary_report):
        runs=TrackerCertification.objects.all()
        assert SHIFTER1_USERNAME == runs.shifters()[0].username

    def test_week_number(self):
        runs=TrackerCertification.objects.all()
        ret = runs.week_number()
        assert "" == ret

        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=1234, run_type="cosmics"), reconstruction="express"),
            pixel="good",
            strip="good",
            tracking="good",
            date="2019-6-10"
        )

        runs=TrackerCertification.objects.all()
        ret = runs.week_number()
        assert 24 == ret

        mixer.blend(
            "certifier.TrackerCertification",
            runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend(OmsRun, run_number=1274, run_type="cosmics"), reconstruction="express"),
            pixel="good",
            strip="good",
            tracking="good",
            date="2019-7-10"
        )

        runs=TrackerCertification.objects.all()
        ret = runs.week_number()
        assert "24-28" == ret

    def test_order_by_run_number(self, shifter, runs_for_summary_report):
        runs=TrackerCertification.objects.all().order_by_run_number()
        assert 300000 == runs[0].runreconstruction.run.run_number
        assert 300024 == runs[len(runs)-1].runreconstruction.run.run_number

    def test_order_by_date(self, runs_for_slr):
        runs=TrackerCertification.objects.all().order_by_date()
        assert 1 == runs[0].runreconstruction.run.run_number
        assert 15 == runs[len(runs)-1].runreconstruction.run.run_number

    def test_compare_with_run_registry_above_500(self):
        create_runs(501, 1, "collisions", "express")
        runs=TrackerCertification.objects.all()
        deviating, corresponding = runs.compare_with_run_registry()
        assert 501 == len(deviating)
        assert 501 == len(corresponding)

    def test_compare_with_run_registry(self):
        create_runs(3, 1, "collisions", "express")
        runs=TrackerCertification.objects.all()
        deviating, corresponding = runs.compare_with_run_registry()
        assert 3 == len(deviating)
        assert 3 == len(corresponding)

    def test_matches_with_run_registry(self):
        create_runs(2, 1, "collisions", "express")
        runs=TrackerCertification.objects.all()
        ret = runs.matches_with_run_registry()
        assert False == ret

    @pytest.mark.skip(reason="skipped due to travis not being able to run it")
    def test_annotate_fill_number(self, shifter, runs_for_summary_report):
        runs=TrackerCertification.objects.all()
        runs.annotate_fill_number()
        assert 6016 == runs[8].fill_number
