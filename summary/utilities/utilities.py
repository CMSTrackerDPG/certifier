import sys
import logging
from textwrap import wrap
from prettytable import PrettyTable, ALL
from shiftleader.utilities.utilities import to_date
from listruns.utilities.utilities import is_valid_date
from certifier.models import TrackerCertification

logger = logging.getLogger(__name__)


def set_terminal_size(width, height):
    """
    Dirty(?) solution of forcing the terminal size to a specific
    size so that terminaltables behave
    """
    sys.stdout.write(f"\x1b[8;{height};{width}t")


def get_wrapped_string(string: str, max_width: int) -> str:
    """
    Use textwrap to wrap long strings, given an max_width
    """
    if max_width <= 0:
        raise ValueError(f"Max width must be > 0 ({max_width} given)")
    if not isinstance(string, str) or len(string) < max_width:
        return string
    return "\n".join(wrap(string, max_width))


def get_from_summary(summary, runtype=None, reco=None, date=None):
    filtered = summary
    if runtype:
        filtered = [
            item for item in filtered
            if item["runreconstruction__run__run_type"] == runtype
        ]
    if reco:
        filtered = [
            item for item in filtered
            if item["runreconstruction__reconstruction"] == reco
        ]
    if date:
        filtered = [item for item in filtered if item["date"] == to_date(date)]
    return filtered


def get_ascii_table(column_description, data):
    """
    Create a PrettyTable using the header and table data
    passed.

    If table is too wide, try to wrap every line that's too long
    """
    tbl = PrettyTable()
    tbl._max_width = {"Comment": 50}  # Hardcoded value
    tbl.field_names = column_description
    tbl.add_rows(data)
    tbl.hrules = ALL
    return str(tbl)


def get_runs_from_request_filters(request, alert_errors, alert_infos,
                                  alert_filters):

    runs = TrackerCertification.objects.filter(user=request.user)

    date_filter_value = request.GET.get("date", None)

    date_from = request.GET.get("date_range_0", None)
    date_to = request.GET.get("date_range_1", None)
    runs_from = request.GET.get("runs_0", None)
    runs_to = request.GET.get("runs_1", None)

    if date_filter_value:
        if is_valid_date(date_filter_value):
            runs = runs.filter(date=date_filter_value)
            alert_filters.append("Date: " + str(date_filter_value))

        else:
            alert_errors.append("Invalid Date: " + str(date_filter_value))
            return TrackerCertification.objects.none()

    if date_from:
        if is_valid_date(date_from):
            runs = runs.filter(date__gte=date_from)
            alert_filters.append("Date from: " + str(date_from))
        else:
            alert_errors.append("Invalid Date: " + str(date_from))
            return TrackerCertification.objects.none()

    if date_to:
        if is_valid_date(date_to):
            runs = runs.filter(date__lte=date_to)
            alert_filters.append("Date to: " + str(date_to))
        else:
            alert_errors.append("Invalid Date: " + str(date_to))
            return TrackerCertification.objects.none()

    if runs_from:
        try:
            runs = runs.filter(
                runreconstruction__run__run_number__gte=runs_from)
            alert_filters.append("Runs from: " + str(runs_from))
        except:
            alert_errors.append("Invalid Run Number: " + str(runs_from))
            return TrackerCertification.objects.none()

    if runs_to:
        try:
            runs = runs.filter(runreconstruction__run__run_number__lte=runs_to)
            alert_filters.append("Runs to: " + str(runs_to))
        except:
            alert_errors.append("Invalid Run Number: " + str(runs_to))
            return TrackerCertification.objects.none()

    if (not date_filter_value and not date_from and not date_to
            and not runs_from and not runs_to):
        alert_infos.append(
            "No filters applied. Showing every run you have ever certified!")

    return runs.order_by("-runreconstruction__run__run_number")
