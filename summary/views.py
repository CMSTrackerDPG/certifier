import logging
from datetime import datetime
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from summary.forms import SummaryExtraInfoForm
from summary.models import SummaryInfo
from summary.utilities.SummaryReport import SummaryReport
from summary.utilities.utilities import get_runs_from_request_filters

logger = logging.getLogger(__name__)


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

    request.GET = request.GET.copy()

    request.GET["date"] = (
        datetime.now().strftime("%Y-%m-%d")
        if not "date" in request.GET
        else request.GET["date"]
    )

    # Filters TrackerCertification objects based on
    # GET filters
    runs = get_runs_from_request_filters(
        request, alert_errors, alert_infos, alert_filters
    )
    logger.debug(f"Generating summary for {runs.count()} runs")

    summary = SummaryReport(runs)

    # Get run numbers from QuerySet
    runs_list = [r[0] for r in runs.values_list("runreconstruction__run__run_number")]

    print("!!!!!!!!", runs_list)
    summary_db_instance, _ = SummaryInfo.objects.get_or_create(runs=runs_list)
    form = SummaryExtraInfoForm(instance=summary_db_instance)

    context = {
        "refs": summary.reference_runs(),
        "runs": summary.runs_checked_per_type(),
        "tk_maps": summary.tracker_maps_per_type(),
        "certified_runs": summary.certified_runs_per_type(),
        "sums": summary.sum_of_quantities_per_type(),
        "alert_errors": alert_errors,
        "alert_infos": alert_infos,
        "alert_filters": alert_filters,
        "form": form,
    }

    return render(request, "summary/summary.html", context)


class SummaryExtraInfoView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View that handles extra info submitted by shifters for a specific summary.

    A summary is uniquely identified by the list of runs it is composed of.
    """

    form = SummaryExtraInfoForm

    def test_func(self):
        """
        Function used by the UserPassesTestMixin to
        test rights before allowing acess to the View
        """
        return (
            hasattr(self.request.user, "has_shifter_rights")
            and self.request.user.has_shifter_rights
        )

    def post(self, request, *args, **kwargs):
        response = {"success": True}
        return JsonResponse(response)
