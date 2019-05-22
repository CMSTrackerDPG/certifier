from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from certifier.models import TrackerCertification
from django_tables2 import SingleTableMixin
from tables.tables import ShiftleaderTrackerCertificationTable, DeletedTrackerCertificationTable
from django_filters.views import FilterView
from certifier.forms import CertifyForm
from listruns.utilities.utilities import (
    request_contains_filter_parameter,
    get_this_week_filter_parameter,
    get_runs_from_request_filters,
)
from listruns.filters import (
    TrackerCertificationFilter,
    ComputeLuminosityTrackerCertificationFilter,
    RunsFilter,
)
from shiftleader.filters import ShiftLeaderTrackerCertificationFilter
from shiftleader.utilities.ShiftLeaderReport import ShiftLeaderReport
from shiftleader.utilities.SummaryReport import SummaryReport
from checklists.models import Checklist
# Create your views here.

@login_required
def shiftleader_view(request):
    """
    if no filter parameters are specified than every run from every user will be listed
    to prevent this we make sure that at least one filter is applied.

    if someone wants to list all runs form all users then he has to specify that explicitly
    in the filter (setting everything to nothing)
    """
    print(request)
    if request_contains_filter_parameter(request):
        return ShiftLeaderView.as_view()(request=request)
    return HttpResponseRedirect("/shiftleader/%s" % get_this_week_filter_parameter())

@login_required
def summaryView(request):
    """
    Accumulates information that is needed in the Run Summary
    stores it in the 'context' object and passes that object to summary.html
    where it is then displayed.
    """

    alert_errors = []
    alert_infos = []
    alert_filters = []

    runs = get_runs_from_request_filters(
        request, alert_errors, alert_infos, alert_filters
    )

    summary = SummaryReport(runs)

    context = {
        "refs": summary.reference_runs(),
        "runs": summary.runs_checked_per_type(),
        "tk_maps": summary.tracker_maps_per_type(),
        "certified_runs": summary.certified_runs_per_type(),
        "sums": summary.sum_of_quantities_per_type(),
        "alert_errors": alert_errors,
        "alert_infos": alert_infos,
        "alert_filters": alert_filters,
    }

    return render(request, "shiftleader/summary.html", context)

# TODO lazy load summary
@method_decorator(login_required, name="dispatch")
class ShiftLeaderView(SingleTableMixin, FilterView):
    table_class = ShiftleaderTrackerCertificationTable
    model = TrackerCertification
    template_name = "shiftleader/shiftleader.html"
    filterset_class = ShiftLeaderTrackerCertificationFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = SummaryReport(self.filterset.qs)
        context["slreport"] = ShiftLeaderReport(self.filterset.qs)
        context["deleted_runs"] = DeletedTrackerCertificationTable(
            TrackerCertification.all_objects.dead().order_by("-runreconstruction__run__run_number")
        )
        try:
            context["slchecklist"] = Checklist.objects.get(identifier="shiftleader")
        except Checklist.DoesNotExist:
            # shift leader checklist has not been created yet.
            pass

        '''
        deviating, corresponding = self.filterset.qs.compare_with_run_registry()

        if deviating:
            context["runinfo_comparison_table"] = RunRegistryComparisonTable(deviating)
            context["run_registry_comparison_table"] = RunRegistryComparisonTable(
                corresponding
            )
        '''
        return context

@method_decorator(login_required, name="dispatch")
class DeleteRun(generic.DeleteView):
    """
    Deletes a specific Run from the RunInfo table
    """

    model = TrackerCertification
    form_class = CertifyForm
    success_url = "/shiftleader/"
    template_name_suffix = "_delete_form"

@login_required
def restore_run_view(request, pk, run_number, reco):
    try:
        trackerCertification = TrackerCertification.all_objects.get(pk=pk)
    except RunInfo.DoesNotExist:
        raise Http404("The run with the id {} doesnt exist".format(pk))

    if request.method == "POST":
        trackerCertification.restore()
        return HttpResponseRedirect("/shiftleader/")

    return render(request, "shiftleader/restore.html", {"trackerCertification": trackerCertification})

@login_required
def hard_delete_run_view(request, pk, run_number, reco):
    try:
        trackerCertification = TrackerCertification.all_objects.get(pk=pk)
    except RunInfo.DoesNotExist:
        raise Http404("The run with the id {} doesnt exist".format(pk))

    if request.method == "POST":
        trackerCertification.hard_delete()
        return HttpResponseRedirect("/shiftleader/")

    return render(request, "shiftleader/hard_delete.html", {"trackerCertification": trackerCertification})

