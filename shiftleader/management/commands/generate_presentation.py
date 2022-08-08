from datetime import date, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from shiftleader.utilities.utilities import DateConverter
from shiftleader.utilities.shiftleader_report_presentation import (
    ShiftLeaderReportPresentation,
)
from certifier.models import TrackerCertification


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("date_from", type=str)
        parser.add_argument("date_to", type=str)

    def handle(self, *args, **options):
        date_from = options["date_from"]
        date_to = options["date_to"]
        try:
            date_from = DateConverter().to_python(date_from)
            date_to = DateConverter().to_python(date_to)
        except ValueError as e:
            raise CommandError(
                f"date_from and date_to must be in the format {DateConverter.regex}"
            )

        p = ShiftLeaderReportPresentation(
            date_from=date_from,
            date_to=date_to,
            requesting_user="",
            certhelper_version=settings.CERTHELPER_VERSION,
            name_shift_leader="",
            names_shifters=[],
            names_oncall=[],
        )
        p.save()
