from django.utils import timezone
from django.shortcuts import render, redirect
from openruns.models import OpenRuns
from tables.tables import OpenRunsTable
from openruns.utilities import get_range_of_open_runs, get_specific_open_runs
from django_tables2 import RequestConfig
from django.http import HttpResponse
from django.db.models import Case, When
import json
import re

def openruns(request):
    context = {}

    if request.method == 'GET':
        run_number = request.GET.get("run_number", None)
        reco = request.GET.get("reco", None)

        if run_number and reco:
            response = redirect("/certify/{}/{}".format(run_number, reco))
            return response

        if run_number:
            response = redirect("/certify/{}".format(run_number))
            return response

    if request.method == 'POST':

        min_run_number = request.POST.get("min", None)
        max_run_number = request.POST.get("max", None)

        runs_list = request.POST.get("list", None)

        runs_search_limit = 20

        if runs_list:
            try:
                runs_list = list(map(int, re.split(" , | ,|, |,| ", re.sub('\s+', ' ', runs_list).lstrip().rstrip())))
            except ValueError:
                context = {"message": "Run list should contains only numbers of runs separated by comma or space"}
                return render(request, "certifier/404.html", context)

        if min_run_number and max_run_number and not runs_list:
            number_of_runs = int(max_run_number) - int(min_run_number)
            if number_of_runs >= runs_search_limit:
                context = {"message": "Please search for less than {} runs".format(runs_search_limit)}
                #return render(request, "certifier/404.html", context)
            else:
                get_range_of_open_runs(min_run_number,max_run_number, request.user)

        elif len(runs_list) >= runs_search_limit:
            context = {"message": "Please search for less than {} runs".format(runs_search_limit)}
            #return render(request, "certifier/404.html", context)
        
        else:
            get_specific_open_runs(runs_list, request.user)

    today = timezone.now().strftime("%Y-%m-%d")

    show_openruns = OpenRuns.objects.filter(date_retrieved=today).order_by("-run_number")

    openruns_table = OpenRunsTable(show_openruns)
    openruns_table.request = request

    RequestConfig(request).configure(openruns_table)

    context["openruns_table"] = openruns_table

    return render(request, "openruns/openruns.html", context)

