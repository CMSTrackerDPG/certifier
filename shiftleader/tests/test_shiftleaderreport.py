import math
import pytest
import os
from django.utils import timezone
from certifier.models import TrackerCertification
from shiftleader.utilities.ShiftLeaderReport import ShiftLeaderReport, ShiftLeaderReportDay
from shiftleader.utilities.utilities import to_date
from utilities.utilities import create_runs

pytestmark = pytest.mark.django_db


class TestShiftLeaderReport:
    def test_weekly_certification(self, runs_for_slr):
        runs = TrackerCertification.objects.all()
        report = ShiftLeaderReport(runs)

        assert report.collisions().express().total_number() == 8
        assert report.collisions().prompt().total_number() == 3
        assert report.cosmics().express().total_number() == 7
        assert report.cosmics().prompt().total_number() == 1

        assert math.isclose(161301.363, report.collisions().express().integrated_luminosity(), abs_tol=0.1)
        assert report.prompt().collisions().integrated_luminosity() == 123133.554
        assert report.express().cosmics().integrated_luminosity() == 0.1234
        assert report.cosmics().prompt().integrated_luminosity() == 0

        assert report.bad().collisions().express().total_number() == 0
        assert report.prompt().bad().collisions().total_number() == 3
        assert report.cosmics().bad().express().total_number() == 2
        assert report.bad().prompt().cosmics().total_number() == 1

        assert report.bad().collisions().express().integrated_luminosity() == 0
        assert report.bad().collisions().prompt().integrated_luminosity() == 123133.554
        assert report.bad().cosmics().express().integrated_luminosity() == 0
        assert report.bad().cosmics().prompt().integrated_luminosity() == 0

    def test_day_by_day(self, runs_for_slr):
        runs = TrackerCertification.objects.all()
        report = ShiftLeaderReport(runs)

        day_by_day = report.day_by_day()

        assert day_by_day[0].name() == "Monday"
        assert day_by_day[1].name() == "Tuesday"
        assert day_by_day[2].name() == "Thursday"
        assert day_by_day[3].name() == "Friday"
        assert day_by_day[4].name() == "Sunday"

        assert to_date("2018-05-14") == day_by_day[0].date()
        assert day_by_day[1].date() == to_date("2018-05-15")
        assert day_by_day[2].date() == to_date("2018-05-17")
        assert day_by_day[3].date() == to_date("2018-05-18")
        assert day_by_day[4].date() == to_date("2018-05-20")

        day = day_by_day[0]

        assert day.collisions().express().total_number() == 3
        assert day.collisions().prompt().total_number() == 1
        assert day.cosmics().express().total_number() == 3
        assert day.cosmics().prompt().total_number() == 1

        assert day.collisions().express().integrated_luminosity() == 5212
        assert day.prompt().collisions().integrated_luminosity() == 1.234
        assert day.express().cosmics().integrated_luminosity() == 0.1234
        assert day.cosmics().prompt().integrated_luminosity() == 0

        assert day.bad().collisions().express().total_number() == 0
        assert day.prompt().bad().collisions().total_number() == 1
        assert day.cosmics().bad().express().total_number() == 1
        assert day.bad().prompt().cosmics().total_number() == 1

        assert day.bad().collisions().express().integrated_luminosity() == 0
        assert day.bad().collisions().prompt().integrated_luminosity() == 1.234
        assert day.bad().cosmics().express().integrated_luminosity() == 0
        assert day.bad().cosmics().prompt().integrated_luminosity() == 0

        assert 5 == len(report.day_by_day())

        day = day_by_day[1]

        assert day.collisions().express().total_number() == 1
        assert day.collisions().prompt().total_number() == 0
        assert day.cosmics().express().total_number() == 0
        assert day.cosmics().prompt().total_number() == 0

        assert day.collisions().express().integrated_luminosity() == 423.24
        assert day.prompt().collisions().integrated_luminosity() == 0
        assert day.express().cosmics().integrated_luminosity() == 0
        assert day.cosmics().prompt().integrated_luminosity() == 0

        assert day.bad().collisions().express().total_number() == 0
        assert day.prompt().bad().collisions().total_number() == 0
        assert day.cosmics().bad().express().total_number() == 0
        assert day.bad().prompt().cosmics().total_number() == 0

        assert day.bad().collisions().express().integrated_luminosity() == 0
        assert day.bad().collisions().prompt().integrated_luminosity() == 0
        assert day.bad().cosmics().express().integrated_luminosity() == 0
        assert day.bad().cosmics().prompt().integrated_luminosity() == 0

        day = day_by_day[2]

        assert day.collisions().express().total_number() == 0
        assert day.collisions().prompt().total_number() == 0
        assert day.cosmics().express().total_number() == 3
        assert day.cosmics().prompt().total_number() == 0

        assert day.collisions().express().integrated_luminosity() == 0
        assert day.prompt().collisions().integrated_luminosity() == 0
        assert day.express().cosmics().integrated_luminosity() == 0
        assert day.cosmics().prompt().integrated_luminosity() == 0

        assert day.bad().collisions().express().total_number() == 0
        assert day.prompt().bad().collisions().total_number() == 0
        assert day.cosmics().bad().express().total_number() == 1
        assert day.bad().prompt().cosmics().total_number() == 0

        assert day.bad().collisions().express().integrated_luminosity() == 0
        assert day.bad().collisions().prompt().integrated_luminosity() == 0
        assert day.bad().cosmics().express().integrated_luminosity() == 0
        assert day.bad().cosmics().prompt().integrated_luminosity() == 0

        day = day_by_day[3]

        assert day.collisions().express().total_number() == 2
        assert day.collisions().prompt().total_number() == 0
        assert day.cosmics().express().total_number() == 0
        assert day.cosmics().prompt().total_number() == 0

        assert day.collisions().express().integrated_luminosity() == 154543 + 124.123
        assert day.prompt().collisions().integrated_luminosity() == 0
        assert day.express().cosmics().integrated_luminosity() == 0
        assert day.cosmics().prompt().integrated_luminosity() == 0

        assert day.bad().collisions().express().total_number() == 0
        assert day.prompt().bad().collisions().total_number() == 0
        assert day.cosmics().bad().express().total_number() == 0
        assert day.bad().prompt().cosmics().total_number() == 0

        assert day.bad().collisions().express().integrated_luminosity() == 0
        assert day.bad().collisions().prompt().integrated_luminosity() == 0
        assert day.bad().cosmics().express().integrated_luminosity() == 0
        assert day.bad().cosmics().prompt().integrated_luminosity() == 0

        day = day_by_day[3]

        assert day.collisions().express().total_number() == 2
        assert day.collisions().prompt().total_number() == 0
        assert day.cosmics().express().total_number() == 0
        assert day.cosmics().prompt().total_number() == 0

        assert day.collisions().express().integrated_luminosity() == 154543 + 124.123
        assert day.prompt().collisions().integrated_luminosity() == 0
        assert day.express().cosmics().integrated_luminosity() == 0
        assert day.cosmics().prompt().integrated_luminosity() == 0

        assert day.bad().collisions().express().total_number() == 0
        assert day.prompt().bad().collisions().total_number() == 0
        assert day.cosmics().bad().express().total_number() == 0
        assert day.bad().prompt().cosmics().total_number() == 0

        assert day.bad().collisions().express().integrated_luminosity() == 0
        assert day.bad().collisions().prompt().integrated_luminosity() == 0
        assert day.bad().cosmics().express().integrated_luminosity() == 0
        assert day.bad().cosmics().prompt().integrated_luminosity() == 0

        day = day_by_day[4]

        assert day.collisions().express().total_number() == 2
        assert day.collisions().prompt().total_number() == 2
        assert day.cosmics().express().total_number() == 1
        assert day.cosmics().prompt().total_number() == 0

        assert day.collisions().express().integrated_luminosity() == 999
        assert day.prompt().collisions().integrated_luminosity() == 123132.32
        assert day.express().cosmics().integrated_luminosity() == 0
        assert day.cosmics().prompt().integrated_luminosity() == 0

        assert day.bad().collisions().express().total_number() == 0
        assert day.prompt().bad().collisions().total_number() == 2
        assert day.cosmics().bad().express().total_number() == 0
        assert day.bad().prompt().cosmics().total_number() == 0

        assert day.bad().collisions().express().integrated_luminosity() == 0
        assert day.bad().collisions().prompt().integrated_luminosity() == 123132.32
        assert day.bad().cosmics().express().integrated_luminosity() == 0
        assert day.bad().cosmics().prompt().integrated_luminosity() == 0

    def test_list_of_run_numbers(self):
        create_runs(5, 1, "collisions", "express", good=True)
        create_runs(4, 6, "collisions", "express", good=False)
        create_runs(3, 10, "collisions", "prompt", good=True)
        create_runs(3, 15, "collisions", "prompt", good=False)
        create_runs(5, 21, "cosmics", "express", good=True)
        create_runs(4, 26, "cosmics", "express", good=False)
        create_runs(3, 30, "cosmics", "prompt", good=True)
        create_runs(3, 35, "cosmics", "prompt", good=False)
        create_runs(2, 38, "cosmics", "rereco", good=False)
        create_runs(2, 40, "cosmics", "rereco", good=False)

        runs = TrackerCertification.objects.all().order_by("run_number")
        report = ShiftLeaderReport(runs)

        assert [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
        ] == report.collisions().express().run_numbers()
        assert [10, 11, 12, 15, 16, 17] == report.collisions().prompt().run_numbers()
        assert [
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
        ] == report.cosmics().express().run_numbers()
        assert [30, 31, 32, 35, 36, 37] == report.cosmics().prompt().run_numbers()

        assert [1, 2, 3, 4, 5] == report.collisions().express().good().run_numbers()
        assert [10, 11, 12] == report.collisions().prompt().good().run_numbers()
        assert [21, 22, 23, 24, 25] == report.cosmics().express().good().run_numbers()
        assert [30, 31, 32] == report.cosmics().prompt().good().run_numbers()

        assert [6, 7, 8, 9] == report.collisions().express().bad().run_numbers()
        assert [15, 16, 17] == report.collisions().prompt().bad().run_numbers()
        assert [26, 27, 28, 29] == report.cosmics().express().bad().run_numbers()
        assert [35, 36, 37] == report.cosmics().prompt().bad().run_numbers()

        assert [38, 39, 40, 41] == report.cosmics().rereco().bad().run_numbers()
        assert [38, 39, 40, 41] == report.cosmics().rereco().bad().run_numbers()

    @pytest.mark.skipif('TRAVIS' in os.environ, reason="skipped due to travis not being able to run it")
    def test_fill_numbers(self):
        create_runs(1, 321177, "cosmics", "express")
        create_runs(1, 321178, "cosmics", "express")
        create_runs(1, 321218, "cosmics", "express")
        create_runs(1, 323500, "cosmics", "express")

        runs = TrackerCertification.objects.all().order_by("run_number")
        report = ShiftLeaderReport(runs)

        assert [7048, 7052] == report.cosmics().express().good().fill_numbers()

    @pytest.mark.skipif('TRAVIS' in os.environ, reason="skipped due to travis not being able to run it")
    def test_fills(self):
        create_runs(1, 321171, "cosmics", "express")
        create_runs(1, 321179, "cosmics", "express")
        create_runs(1, 321181, "cosmics", "express")
        create_runs(1, 321182, "cosmics", "express")
        create_runs(1, 321185, "cosmics", "express")

        runs = TrackerCertification.objects.all().order_by("run_number")
        report = ShiftLeaderReport(runs)

        assert [{'fill_number': 7049, 'run_number': [321185, 321182]}, {'fill_number': 7048, 'run_number': [321181, 321179, 321171]}] == report.cosmics().express().good().fills()

    def test_flag_changed(self):
        today = timezone.now().date

        create_runs(3, 321171, "collisions", "express", good=False, date=today)
        create_runs(3, 321171, "collisions", "prompt", date=today)

        runs = TrackerCertification.objects.all()
        report = ShiftLeaderReportDay(runs)

        assert [321171, 321171, 321172, 321172, 321173, 321173] == report.flag_changed().run_numbers()

    def test_list_of_run_certified(self):
        create_runs(2, 1, "collisions", "express", good=True, date="2018-05-14")
        create_runs(2, 6, "collisions", "express", good=False, date="2018-05-14")
        create_runs(2, 10, "collisions", "prompt", good=True, date="2018-05-15")
        create_runs(2, 15, "collisions", "prompt", good=False, date="2018-05-15")
        create_runs(2, 21, "cosmics", "express", good=True, date="2018-05-14")
        create_runs(2, 26, "cosmics", "express", good=False, date="2018-05-16")
        create_runs(2, 30, "cosmics", "prompt", good=True, date="2018-05-14")
        create_runs(2, 35, "cosmics", "prompt", good=False, date="2018-05-14")

        runs = TrackerCertification.objects.all().order_by("runreconstruction__run__run_number")
        report = ShiftLeaderReport(runs)

        days = report.day_by_day()

        assert [1, 2, 6, 7] == days[0].express().collisions().run_numbers()
        assert [21, 22] == days[0].express().cosmics().run_numbers()
        assert [26, 27] == days[2].express().cosmics().run_numbers()
        assert [10, 11, 15, 16] == days[1].prompt().collisions().run_numbers()
        assert [30, 31, 35, 36] == days[0].prompt().cosmics().run_numbers()
