from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from certifier.models import TrackerCertification
from django_tables2 import SingleTableMixin
from tables.tables import ShiftleaderTrackerCertificationTable, DeletedTrackerCertificationTable, RunRegistryComparisonTable
from django_filters.views import FilterView
from certifier.forms import CertifyForm
from listruns.utilities.utilities import request_contains_filter_parameter
from shiftleader.utilities.utilities import get_this_week_filter_parameter

from listruns.filters import (
    TrackerCertificationFilter,
    ComputeLuminosityTrackerCertificationFilter,
    RunsFilter,
)
from shiftleader.filters import ShiftLeaderTrackerCertificationFilter
from shiftleader.utilities.ShiftLeaderReport import ShiftLeaderReport
from summary.utilities.SummaryReport import SummaryReport
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
    if request_contains_filter_parameter(request):
        return ShiftLeaderView.as_view()(request=request)
    return HttpResponseRedirect("/shiftleader/%s" % get_this_week_filter_parameter())

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

        deviating, corresponding = self.filterset.qs.compare_with_run_registry()

        if deviating:
            context["trackercertification_comparison_table"] = RunRegistryComparisonTable(deviating)
            context["run_registry_comparison_table"] = RunRegistryComparisonTable(
                corresponding
            )

        return context
