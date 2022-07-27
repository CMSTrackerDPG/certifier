from datetime import date, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from shiftleader.utilities.shiftleader_report_presentation import (
    ShiftLeaderReportPresentation,
)
from certifier.models import TrackerCertification


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("year", type=int)
        parser.add_argument("week_number", type=int)

    def handle(self, *args, **options):
        year = options["year"]
        week_number = options["week_number"]

        # Get first day of week requested
        week_start = date.fromisocalendar(year=year, week=week_number, day=1)

        week_end = week_start + timedelta(days=6)

        queryset = TrackerCertification.objects.filter(
            date__gte=week_start,
            date__lte=week_end,
        )
        p = ShiftLeaderReportPresentation(
            requesting_user="",
            certhelper_version=settings.CERTHELPER_VERSION,
            year=year,
            week_number=week_number,
            name_shift_leader="",
            names_shifters=[],
            names_oncall=[],
            certification_queryset=queryset,
        )
        p.save()
