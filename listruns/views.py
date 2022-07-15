import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django_tables2 import RequestConfig
from oms.models import OmsRun, OmsFill
from oms.forms import OmsRunForm, OmsFillForm

from certifier.models import TrackerCertification
from certifier.forms import CertifyFormWithChecklistForm

from tables.tables import TrackerCertificationTable

from listruns.filters import (
    TrackerCertificationFilter,
)
from listruns.utilities.utilities import (
    get_filters_from_request_GET,
    request_contains_filter_parameter,
    get_today_filter_parameter,
)


logger = logging.getLogger(__name__)

# Create your views here.
# @login_required
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
    run_info_list = TrackerCertification.objects.all()

    # This does not seem to be required, the check for disabling the edit button
    # is done upon the django_table creation
    # if request.user.is_authenticated:
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
class UpdateRunView(UpdateView):
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
        context["run_number"] = self.kwargs["run_number"]
        context["reco"] = self.kwargs["reco"]
        context["dataset"] = TrackerCertification.objects.get(
            runreconstruction__run__run_number=self.kwargs["run_number"],
            runreconstruction__reconstruction=self.kwargs["reco"],
        ).dataset
        context["run"] = OmsRun.objects.get(run_number=self.kwargs["run_number"])
        context["omsrun_form"] = OmsRunForm(instance=context["run"])
        context["omsfill_form"] = OmsFillForm(instance=context["run"].fill)
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

    def get(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            messages.warning(request, "You are updating another user's certification.")
        else:
            messages.info(request, "You are updating an exising certification.")
        return super().get(request, *args, **kwargs)

    def post(self, request, pk: int, run_number: int, reco: str = None):

        # Get info on the OmsFill
        omsfill_form = OmsFillForm(request.POST)
        fill = None

        if not request.POST.get("external_info_complete"):
            if OmsFill.objects.filter(
                fill_number=omsfill_form.data["fill_number"]
            ).exists():
                omsfill_form = OmsFillForm(
                    request.POST,
                    instance=OmsFill.objects.get(
                        fill_number=omsfill_form.data["fill_number"]
                    ),
                )

            elif not omsfill_form.is_valid():
                msg = f"OmsFill form has errors! {dict(omsfill_form.errors)}"
                logger.error(msg)
                messages.error(request, msg)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            fill = omsfill_form.save()

            # Assumes OmsRun exists!
            omsrun_form = OmsRunForm(
                request.POST, instance=self.get_object().runreconstruction.run
            )
            if omsrun_form.is_valid():
                run = omsrun_form.save(commit=False)
                run.fill = fill
                run.save()
            else:
                msg = f"OmsRun form has errors! {dict(omsrun_form.errors)}"
                logger.error(msg)
                messages.error(request, msg)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        return super().post(self, request, pk, run_number, reco)

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch method to check if the user that tries to
        update the run has the necessary rights
        """

        if self.same_user_or_shiftleader(request.user):
            return super(UpdateRunView, self).dispatch(request, *args, **kwargs)
        return redirect_to_login(
            request.get_full_path(), login_url=reverse("admin:login")
        )

    def get_success_url(self):
        """
        return redirect url after updating a run
        """
        is_same_user = self.get_object().user.id == self.request.user.id
        return reverse("home:home") if not is_same_user else reverse("listruns:list")
