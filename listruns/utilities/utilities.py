import datetime
import decimal
import re
from django.utils import timezone

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

def get_today_filter_parameter():
    return "?date={}".format(timezone.now().strftime("%Y-%m-%d"))

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
