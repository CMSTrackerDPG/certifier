from django.shortcuts import render
from oms.utils import retrieve_run

# Create your views here.

def plot(request, run_number, reco):
    run = retrieve_run(run_number)
    context = {"run_number": run_number, "reco": reco, "run": run}
    return render(request, "plot/plot.html", context)
