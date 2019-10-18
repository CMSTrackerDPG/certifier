import datetime

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

from listruns.utilities.luminosity import format_integrated_luminosity

register = template.Library()


@register.filter(name='addclass')
def addclass(value, arg): # pragma: no cover
    return value.as_widget(attrs={'class': arg})


@register.filter
def add_label_class(field, class_name): # pragma: no cover
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })


@register.filter(name='addplaceholder')
def addplaceholder(value, arg): # pragma: no cover
    return value.as_widget(attrs={'placeholder': arg})


@register.filter
def dateoffset(value, offset): # pragma: no cover
    """
    Shift a date by given offset.
    Example: dateoffset("2018-10-21", 2) => "2018-10-23"
    """
    newdate = datetime.datetime.strptime(value, '%Y-%m-%d') + timezone.timedelta(offset)
    return newdate.strftime('%Y-%m-%d')


@register.filter
def yyyymmdd_to_ddmmyyyy(value): # pragma: no cover
    if isinstance(value, datetime.date):
        newdate = value
    else:
        newdate = datetime.datetime.strptime(value, '%Y-%m-%d')
    return newdate.strftime('%d-%m-%Y')


@register.filter
def yyyymmdd(value): # pragma: no cover
    return value.strftime('%Y-%m-%d')


@register.filter
def join_good_runs(list_of_run_numbers): # pragma: no cover
    """
    takes a list of run numbers and wraps them in <span class="good-runs">
    """
    if list_of_run_numbers:
        rendered_string = '<span class="good-runs">'
        rendered_string += ", ".join(str(x) for x in list_of_run_numbers)
        rendered_string += '</span>'
        return mark_safe(rendered_string)
    return ""


@register.filter
def join_bad_runs(list_of_run_numbers): # pragma: no cover
    """
    takes a list of run numbers and wraps them in <span class="bad-runs">
    """
    if list_of_run_numbers:
        rendered_string = '<span class="bad-runs">'
        rendered_string += ", ".join(str(x) for x in list_of_run_numbers)
        rendered_string += '</span>'
        return mark_safe(rendered_string)
    return ""


@register.filter
def as_date(yyyy_mm_dd): # pragma: no cover
    """
    :param yyyy_mm_dd: date string
    :return: date object
    """

    try:
        return datetime.datetime.strptime(yyyy_mm_dd, '%Y-%m-%d').date()
    except ValueError as e:
        if yyyy_mm_dd == "":
            return ""
        return e


@register.filter
def user(value, arg): # pragma: no cover
    """
    filetrs the runinfo
    """
    return value.filter(user=arg)


def join_by(items, separator): # pragma: no cover
    return separator.join(items)

@register.filter
def format_luminosity(value): # pragma: no cover
    """
    shows up to 3 Decimal places and removes trailing zeros

    Example:
    >>> format_luminosity("1.4567")
    '1.457'
    >>> format_luminosity("13")
    '13'
    >>> format_luminosity("1.33000000")
    '1.33'

    :param value: integrated luminosity value in /pb
    :return:
    """
    return format_integrated_luminosity(value)
