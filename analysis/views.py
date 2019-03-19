from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.shortcuts import render
from oms.utils import retrieve_run

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


def analyse(request, run_number, reco):
    run = retrieve_run(run_number)
    context = {"run_number": run_number, "reco": reco, "run": run}
    return render(request, "analysis/analyse.html", context)
