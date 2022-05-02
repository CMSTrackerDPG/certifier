import logging
from xml.etree.ElementTree import ParseError
from requests.exceptions import SSLError
from django.http import HttpResponseRedirect, HttpResponseServerError
from django_filters.views import FilterView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django_tables2 import SingleTableMixin
from tables.tables import (
    ShiftleaderTrackerCertificationTable,
    DeletedTrackerCertificationTable,
    RunRegistryComparisonTable,
)
from certifier.models import TrackerCertification

from listruns.utilities.utilities import request_contains_filter_parameter
from shiftleader.utilities.utilities import get_this_week_filter_parameter
from shiftleader.filters import ShiftLeaderTrackerCertificationFilter
from shiftleader.utilities.ShiftLeaderReport import ShiftLeaderReport
from summary.utilities.SummaryReport import SummaryReport
from checklists.models import Checklist


logger = logging.getLogger(__name__)


@user_passes_test(
    lambda user: hasattr(user, "has_shift_leader_rights")
    and user.has_shift_leader_rights,
    redirect_field_name=None,
)
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
            TrackerCertification.all_objects.dead().order_by(
                "-runreconstruction__run__run_number"
            )
        )
        try:
            context["slchecklist"] = Checklist.objects.get(identifier="shiftleader")
        except Checklist.DoesNotExist:
            # shift leader checklist has not been created yet.
            pass
        try:
            deviating, corresponding = self.filterset.qs.compare_with_run_registry()
        except (SSLError, ParseError) as e:
            msg = f"CERN Authentication error ({e})"
            logger.error(msg)
            messages.error(self.request, msg, extra_tags="danger")
            return {}

        if deviating:
            context[
                "trackercertification_comparison_table"
            ] = RunRegistryComparisonTable(deviating)
            context["run_registry_comparison_table"] = RunRegistryComparisonTable(
                corresponding
            )

        return context
