from django.shortcuts import render
from summary.utilities.SummaryReport import SummaryReport
from summary.utilities.utilities import get_runs_from_request_filters
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

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
    request.GET["date"]=datetime.now().strftime("%Y-%m-%d")
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

    return render(request, "summary/summary.html", context)

