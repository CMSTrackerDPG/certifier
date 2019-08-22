from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from users.models import User
from django.shortcuts import render
from oms.utils import retrieve_run
from oms.models import OmsRun
from .analyse import run_principal_component_analysis, run_tsne, run_umap, load_data
from .models import ChartDataModel
import json
from django.utils.safestring import mark_safe
from pandas.compat import StringIO
import pandas as pd
from .jobs.chart_data_load_job import Job

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        data = {
            "hello": "world",
        }
        return Response(data)

def generate_chart_data(data, run_number, reco, chart):
    chart_data = []
    good_runs = {}
    bad_runs = {}
    this_run = {}
    this_data = {}

    good_data = data[data["bad_reason"]=="GOOD"]
    bad_data = data[data["bad_reason"]!="GOOD"]

    good_runs["x"] = list(good_data[chart+"1"])
    good_runs["y"] = list(good_data[chart+"2"])
    good_runs["text"] = list(good_data["run_number"])
    good_runs["mode"] = "markers"
    good_runs["type"] = "scatter"
    good_runs["name"] = "Good"
    good_runs["marker"] = {"size": 8}

    bad_runs["x"] = list(bad_data[chart+"1"])
    bad_runs["y"] = list(bad_data[chart+"2"])
    bad_runs["text"] = list(bad_data["run_number"])
    bad_runs["mode"] = "markers"
    bad_runs["type"] = "scatter"
    bad_runs["name"] = "Bad"
    bad_runs["marker"] = {"size": 8}

    chart_data.append(good_runs)
    chart_data.append(bad_runs)

    try:
        this_data = data[data["run_number"]==run_number][data["reco"]==reco]

        this_run["x"] = list(this_data[chart+"1"])
        this_run["y"] = list(this_data[chart+"2"])
        this_run["text"] = list(this_data["run_number"])
        this_run["mode"] = "markers"
        this_run["type"] = "scatter"
        this_run["name"] = "Current Run ("+str(run_number)+")"
        this_run["marker"] = {"size": 12}

        chart_data.append(this_run)
    except KeyError:
        pass

    return chart_data

def analyse(request, run_number, reco):

    try:
        run = OmsRun.objects.get(run_number=run_number)
    except OmsRun.DoesNotExist:
        run = retrieve_run(run_number)

    try:
        chart_data_instance = ChartDataModel.objects.get()
    except ChartDataModel.DoesNotExist:
        Job.execute(Job())

    chart_data_instance = ChartDataModel.objects.get()
    pca_data = pd.read_csv(StringIO(chart_data_instance.pca_data))
    t_sne_data = pd.read_csv(StringIO(chart_data_instance.t_sne_data))
    umap_data = pd.read_csv(StringIO(chart_data_instance.umap_data))

    pca_chart_data = generate_chart_data(pca_data, run_number, reco, "pca")
    t_sne_chart_data = generate_chart_data(t_sne_data, run_number, reco, "tsne")
    umap_chart_data = generate_chart_data(umap_data, run_number, reco, "umap")

    print(type(pca_data))

    context = { "run_number": run_number,
                "reco": reco, "run": run,
                "pca_data": mark_safe(json.dumps(pca_chart_data)),
                "t_sne_data": mark_safe(json.dumps(t_sne_chart_data)),
                "umap_data": mark_safe(json.dumps(umap_chart_data))
              }
    return render(request, "analysis/analyse.html", context)
