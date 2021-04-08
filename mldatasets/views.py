from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from certifier.models import TrackerCertification, RunReconstruction
from mldatasets.serializers import RunReferenceRunSerializer
from oms.models import OmsRun

def runRefRun_list(request):
    if request.method == 'GET':
        runRefRunsAll = TrackerCertification.objects.all()
        serializer = RunReferenceRunSerializer(runRefRunsAll, many=True)
        return JsonResponse(serializer.data, safe=False)


# def run_list(request):
#     if request.method == 'GET':
#         runsAll = OmsRun.objects.all()
#         serializer = RunSerializer(runsAll, many=True)
#         return JsonResponse(serializer.data, safe=False)
