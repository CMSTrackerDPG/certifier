import re

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView, SingleTableMixin

from certifier.models import TrackerCertification
from certifier.forms import CertifyFormWithChecklistForm

from listruns.tables import TrackerCertificationTable

from listruns.filters import (
    TrackerCertificationFilter,
    ShiftLeaderTrackerCertificationFilter,
    ComputeLuminosityTrackerCertificationFilter,
    RunsFilter,
)
from users.models import User
from listruns.utilities.utilities import (
    get_filters_from_request_GET,
    request_contains_filter_parameter,
    get_this_week_filter_parameter,
    get_today_filter_parameter,
    get_runs_from_request_filters,
    number_string_to_list,
    integer_or_none,
)

# Create your views here.
def listruns(request):
    """
    View to list all certified runs
    """
    if not request_contains_filter_parameter(request):
        return HttpResponseRedirect("/list/%s" % get_today_filter_parameter())

    context = {}

    """
    Make sure that the logged in user can only see his own runs
    In case the user is not logged in show all objects,
    but remove the edit and remove buttons from the tableview.
    """
    if request.user.is_authenticated:
        run_info_list = TrackerCertification.objects.filter(user=request.user)
        run_info_filter = TrackerCertificationFilter(request.GET, queryset=run_info_list)
        table = TrackerCertificationTable(run_info_filter.qs)

    else:
        run_info_list = TrackerCertification.objects.all()
        run_info_filter = TrackerCertificationFilter(request.GET, queryset=run_info_list)
        table = SimpleTrackerCertificationTable(run_info_filter.qs)

    RequestConfig(request).configure(table)

    applied_filters = get_filters_from_request_GET(request)
    filter_parameters = ""
    for key, value in applied_filters.items():
        filter_parameters += "&" if filter_parameters.startswith("?") else "?"
        filter_parameters += key + "=" + value

    context["filter_parameters"] = filter_parameters
    context["table"] = table
    context["filter"] = run_info_filter
    return render(request, "listruns/list.html", context)
