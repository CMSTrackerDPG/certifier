from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from shiftleader.utilities.shiftleader_report_presentation import (
    ShiftLeaderReportPresentation,
)


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("week_number", type=int)

    def handle(self, *args, **options):
        p = ShiftLeaderReportPresentation(
            requesting_user="",
            certhelper_version=settings.CERTHELPER_VERSION,
            week_number=options["week_number"],
            name_shift_leader="",
            names_shifters=[],
            names_oncall=[],
        )
        p.save()
