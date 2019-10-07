from django.utils import timezone
from django.shortcuts import render, redirect
from openruns.models import OpenRuns
from tables.tables import OpenRunsTable
from openruns.utilities import get_open_runs, get_specific_open_runs
from django_tables2 import RequestConfig
from django.http import HttpResponse
import json
import re

def openruns(request):
    context = {}

    if request.method == 'GET':
        run_number = request.GET.get("run_number", None)

        if run_number:
            response = redirect("/certify/{}".format(run_number))
            return response

    if request.method == 'POST':

        min_run_number = request.POST.get("min", None)
        max_run_number = request.POST.get("max", None)

        runs_list = request.POST.get("list", None)
        if runs_list:
            try:
                runs_list = list(map(int, re.split(",| ", runs_list)))
            except ValueError:
                context = {"message": "Run list should contains only numbers of runs separated by comma or space"}
                return render(request, "certifier/404.html", context)


        if min_run_number and max_run_number and not runs_list:
            get_open_runs(min_run_number,max_run_number, request.user)
        else:
            get_specific_open_runs(runs_list, request.user)

    today = timezone.now().strftime("%Y-%m-%d")

    if request.user.is_authenticated:
        show_openruns = OpenRuns.objects.filter(user=request.user, date_retrieved=today)
    else:
        show_openruns = OpenRuns.objects.all(date_retrieved=today)

    openruns_table = OpenRunsTable(show_openruns, order_by="-run_number")

    RequestConfig(request).configure(openruns_table)

    context["openruns_table"] = openruns_table

    return render(request, "openruns/openruns.html", context)

