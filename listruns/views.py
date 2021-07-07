import re

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView, SingleTableMixin

from oms.models import OmsRun

from certifier.models import TrackerCertification
from certifier.forms import CertifyFormWithChecklistForm

from tables.tables import TrackerCertificationTable, SimpleTrackerCertificationTable

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
    get_today_filter_parameter,
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
        run_info_list = TrackerCertification.objects.all()
        run_info_filter = TrackerCertificationFilter(request.GET, queryset=run_info_list)
        table = TrackerCertificationTable(run_info_filter.qs, order_by="-date")

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

@method_decorator(login_required, name="dispatch")
class UpdateRun(generic.UpdateView):
    """
    Updates a specific Run from the TrackerCertification table
    """
    model = TrackerCertification
    form_class = CertifyFormWithChecklistForm
    template_name = "certifier/certify.html"

    def get_context_data(self, **kwargs):
        """
        Add extra data for the template
        """

        context = super().get_context_data(**kwargs)
        context["checklist_not_required"] = True
        context["run_number"]=self.kwargs["run_number"]
        context["reco"]=self.kwargs["reco"]
        context["dataset"]=TrackerCertification.objects.get(
                runreconstruction__run__run_number=self.kwargs["run_number"],
                runreconstruction__reconstruction=self.kwargs["reco"]).dataset
        context["run"]=OmsRun.objects.get(run_number=self.kwargs["run_number"])
        return context

    def same_user_or_shiftleader(self, user):
        """
        Checks if the user trying to edit the run is the same user
        that created the run, has at least shift leader rights
        or is a super user (admin)
        """
        return (
            self.get_object().user.id == user.id
            or user.is_superuser
            or user.has_shift_leader_rights
        )

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the user that tries to update the run has the necessary rights
        """
        if self.same_user_or_shiftleader(request.user):
            return super(UpdateRun, self).dispatch(request, *args, **kwargs)
        return redirect_to_login(
            request.get_full_path(), login_url=reverse("admin:login")
        )

    def get_success_url(self):
        """
        return redirect url after updating a run
        """
        is_same_user = self.get_object().user.id == self.request.user.id
        return reverse("home:home") if not is_same_user else reverse("listruns:list")


