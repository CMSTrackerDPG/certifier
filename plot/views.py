from django.shortcuts import render
from oms.utils import retrieve_run
from django.contrib.auth.decorators import login_required
from oms.models import OmsRun

# Create your views here.

@login_required
def plot(request, run_number, reco):
    try:
        run = OmsRun.objects.get(run_number=run_number)
    except OmsRun.DoesNotExist:
        run = retrieve_run(run_number)

    context = {"run_number": run_number, "reco": reco, "run": run}
    return render(request, "plot/plot.html", context)
