import datetime
import decimal
import re
from django.utils import timezone
from django.utils.safestring import mark_safe
from certifier.models import TrackerCertification

def get_ascii_table(column_description, data):
    table = AsciiTable([column_description] + data)
    table.inner_row_border = True
    return table.table

def to_weekdayname(date, formatstring="%Y-%m-%d"):
    return to_date(date, formatstring).strftime("%A")

def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except:
        return False


def get_date_string(year, month, day):
    """"
    returns empty string if date is invalid
    returns YYYY-MM-DD if date is valid
    """

    datestring = None

    if year and month and day:  # if attributes exist
        if (
            int(year) in range(1900, 3000)
            and int(month) in range(1, 13)
            and int(day) in range(1, 32)
        ):
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
            datestring = year + "-" + month + "-" + day

    if is_valid_date(datestring):
        return datestring
    return ""


def get_filters_from_request_GET(request):
    filter_candidates = ["date_range_min", "date_range_max", "runs_min", "runs_max", "type"]
    applied_filters = {}
    for candidate in filter_candidates:
        tmp = request.GET.get(candidate, "")
        if tmp != "" and tmp != 0:
            if (
                candidate.startswith("date_range")
                and is_valid_date(tmp)
            ):
                applied_filters[candidate] = tmp

    year = request.GET.get("date_year", "")
    month = request.GET.get("date_month", "")
    day = request.GET.get("date_day", "")

    the_date = get_date_string(year, month, day)

    # TODO solve conflict between two dates set
    if request.GET.get("date", ""):
        the_date = request.GET.get("date", "")

    if the_date:
        applied_filters["date"] = the_date

    return applied_filters


def is_valid_id(primary_key, Classname):
    try:
        if Classname.objects.filter(pk=primary_key):
            return True
    except:
        return False
    return False


def request_contains_filter_parameter(request):
    for candidate in [
        "options",
        "category",
        "runs",
        "type",
        "date",
        "user",
        "run_number",
        "problem_categories",
    ]:
        for word in request.GET:
            if candidate in word:
                return True
    return False


def get_this_week_filter_parameter():
    start_of_week = timezone.now() - timezone.timedelta(timezone.now().weekday())
    end_of_week = start_of_week + timezone.timedelta(6)

    date_gte = (
        str(start_of_week.year)
        + "-"
        + str(start_of_week.month)
        + "-"
        + str(start_of_week.day)
    )
    date_lte = (
        str(end_of_week.year)
        + "-"
        + str(end_of_week.month)
        + "-"
        + str(end_of_week.day)
    )

    get_parameters = "?date__gte=" + str(date_gte)
    get_parameters += "&date__lte=" + str(date_lte)

    return get_parameters


def get_today_filter_parameter():
    return "?date={}".format(timezone.now().strftime("%Y-%m-%d"))

'''
def get_runs_from_request_filters(request, alert_errors, alert_infos, alert_filters):
    from certifier.models import TrackerCertification

    runs = TrackerCertification.objects.filter(user=request.user)

    date_filter_value = request.GET.get("date", None)

    date_from = request.GET.get("date_range_0", None)
    date_to = request.GET.get("date_range_1", None)
    runs_from = request.GET.get("runs_0", None)
    runs_to = request.GET.get("runs_1", None)
    type_id = request.GET.get("type", None)

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
            runs = runs.filter(run_number__gte=runs_from)
            alert_filters.append("Runs from: " + str(runs_from))
        except:
            alert_errors.append("Invalid Run Number: " + str(runs_from))
            return TrackerCertification.objects.none()

    if runs_to:
        try:
            runs = runs.filter(run_number__lte=runs_to)
            alert_filters.append("Runs to: " + str(runs_to))
        except:
            alert_errors.append("Invalid Run Number: " + str(runs_to))
            return TrackerCertification.objects.none()

    if (
        not date_filter_value
        and not date_from
        and not date_to
        and not runs_from
        and not runs_to
    ):
        alert_infos.append(
            "No filters applied. Showing every run you have ever certified!"
        )

    return runs
'''

def render_component(component, component_lowstat): # pragma: no cover
    """
    Renders the component (Pixel/ SiStrip/ Tracking) for the TrackerCertificationTable

    If lowstat is checked then "Lowstat" is displayed instead of Good/Bad/Excluded
    If the Component is good, then the color will be green, otherwise red.

    This should lead to a similar behavior as in the RunRegistry
    """
    component_rating = component.lower()
    css_class = None

    if component_rating == "good" or component_rating == "lowstat":
        css_class = "good-component"
    elif component_rating == "bad":
        css_class = "bad-component"
    elif component_rating == "excluded":
        css_class = "excluded-component"

    component_value = component

    if component_lowstat is True and component_rating != "excluded":
        component_value = "Lowstat"

    if css_class:
        return mark_safe(
            '<div class="{}">{}</div>'.format(css_class, component_value.title())
        )
    return component


def render_trackermap(trackermap): # pragma: no cover
    if trackermap == "Missing":
        return mark_safe('<div class="bad-component">{}</div>'.format(trackermap))
    return trackermap


def render_boolean_cell(value): # pragma: no cover
    boolean_value = False if value is False or value == "0" or value == 0 else True
    print("{} {}".format(value, boolean_value))
    glyphicon = "ok" if boolean_value else "remove"

    html = '<span class="glyphicon glyphicon-{}"></span>'.format(glyphicon, glyphicon)

    return mark_safe(html)

def decimal_or_none(number):
    """
    Returns the number casted as Decimal or None if it is not a number
    """
    try:
        decimal_number = decimal.Decimal(number)
        return decimal_number if decimal_number.is_finite() else None
    except (decimal.InvalidOperation, ValueError, TypeError):
        return None


def integer_or_none(number):
    """
    Returns the number casted as int or None if casting failed.
    """
    try:
        return int(float(number))
    except (ValueError, TypeError):
        return None


def boolean_or_none(value):
    """
    Returns the value casted as boolean or None if casting failed.

    "true" -> True
    "tRuE" -> True
    "false" -> False
    "" -> None
    "abc" -> None
    0 -> False
    "1" -> True
    1 -> True
    2 -> None
    """
    if isinstance(value, bool):
        return value
    try:
        lower_val = value.lower()
        if lower_val in ["true", "false"]:
            return lower_val == "true"
    except AttributeError:
        pass

    int_val = integer_or_none(value)
    if int_val in [0, 1]:
        return int_val == 1

    return None
