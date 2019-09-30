from django.shortcuts import render, redirect
from openruns.models import OpenRuns
from tables.tables import OpenRunsTable
from openruns.utilities import get_open_runs
from django_tables2 import RequestConfig

def openruns(request):
    context = {}

    run_number = request.GET.get("run_number", None)
    min_run_number = request.POST.get("min", None)
    max_run_number = request.POST.get("max", None)

    if run_number:
        response = redirect("/certify/{}".format(run_number))
        return response

    if min_run_number and max_run_number:
        get_open_runs(min_run_number,max_run_number, request.user)

    if request.user.is_authenticated:
        openruns = OpenRuns.objects.filter(user=request.user)
    else:
        openruns = OpenRuns.objects.all()

    openruns_table = OpenRunsTable(openruns, order_by="-run_number")

    RequestConfig(request).configure(openruns_table)

    context["openruns_table"] = openruns_table

    return render(request, "openruns/openruns.html", context)

