import pytest

from certifier.models import TrackerCertification
from summary.utilities.SummaryReport import SummaryReport

pytestmark = pytest.mark.django_db


class TestSummaryReport:
    def test_summaryreport(self, shifter, runs_for_summary_report):
        summary = SummaryReport(
            TrackerCertification.objects.all().order_by(
                "runreconstruction__run__run_number"
            )
        )

        refs = summary.reference_runs().order_by("run__run_number")
        assert 4 == len(refs)
        assert 300250 == refs[3].run_number
        assert 300200 == refs[2].run_number
        assert 300150 == refs[1].run_number
        assert 300100 == refs[0].run_number

        runs_checked = summary.runs_checked_per_type()

        assert 4 == len(runs_checked)
        assert (
            "Type 1: express collisions 3.8 T Proton-Proton 13 TeV /StreamExpress/Run2018A-Express-v1/DQMIO"
            in runs_checked[0]
        )
        assert (
            "Type 2: prompt collisions 3.8 T Proton-Proton 13 TeV /ZeroBias/Run2018D-PromptReco-v2/DQMIO"
            in runs_checked[1]
        )
        assert (
            "Type 3: express cosmics 3.8 T Cosmics 0 TeV /StreamExpressCosmics/Run2018D-Express-v1/DQMIO"
            in runs_checked[2]
        )
        assert (
            "Type 4: prompt cosmics 3.8 T Cosmics 0 TeV /Cosmics/Run2018D-PromptReco-v2/DQMIO"
            in runs_checked[3]
        )

        tracker_maps = summary.tracker_maps_per_type()
        assert 4 == len(tracker_maps)

        assert (
            """Type 1
 Exists: 300001 300005 300018
 Missing: 300010 300011\n"""
            == tracker_maps[0]
        )

        assert (
            """Type 2
 Exists: 300002 300014 300016 300020 300025
 Missing: 300006 300013 300015 300019 300022\n"""
            == tracker_maps[1]
        )

        assert "Type 3" in tracker_maps[2]
        assert "Missing: 300003 300004 300021" in tracker_maps[2]
        assert "Exists: 300009 300023" in tracker_maps[2]

        assert (
            """Type 4
 Exists: 300000 300012
 Missing: 300007 300008 300017 300024\n"""
            == tracker_maps[3]
        )

        certified_runs = summary.certified_runs_per_type()
        assert 4 == len(certified_runs)

        assert "Type 1" in certified_runs[0]
        assert "Bad: 300001 300005 300010 300011 300018" in certified_runs[0]
        assert "" in certified_runs[0]

        assert "Type 2" in certified_runs[1]
        assert (
            "Bad: 300002 300006 300013 300014 300016 300019 300020 300022 300025"
            in certified_runs[1]
        )
        assert "Good: 300015" in certified_runs[1]

        assert "Type 3" in certified_runs[2]
        assert "Good: 300003 300009" in certified_runs[2]
        assert "Bad: 300004 300021 300023" in certified_runs[2]

        assert "Type 4" in certified_runs[3]
        assert "Bad: 300000 300008 300012 300017 300024" in certified_runs[3]
        assert "Good: 300007" in certified_runs[3]

        sums = summary.sum_of_quantities_per_type()

        assert 4 == len(sums)

        assert "| Type 1 | Sum of LS | Sum of int. luminosity |" in sums[0]
        assert "| Bad    | 3424      | 3534.83 /pb            |" in sums[0]

        assert "| Type 2 | Sum of LS | Sum of int. luminosity |" in sums[1]
        assert "| Bad    | 4487      | 5316" in sums[1]
        assert "| Good   | 265       | 432" in sums[1]

        assert "| Type 3 | Sum of LS | Sum of int. luminosity |" in sums[2]
        assert "| Good   | 708       | 0" in sums[2]
        assert "| Bad    | 1015      | 0" in sums[2]

        assert "| Type 4 | Sum of LS | Sum of int. luminosity |" in sums[3]
        assert "| Bad    | 2091      | 0" in sums[3]
        assert "| Good   | 341       | 0" in sums[3]
