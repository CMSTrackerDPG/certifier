from django.shortcuts import render

# Create your views here.
from wbmcrawlr import oms
from django.http import JsonResponse


def run(request, run_number):
    try:
        run = oms.get_runs(run_number, run_number)[0]  # TODO Update get_runs to flatten
    except IndexError:
        run = {}
    return JsonResponse(run)


def fill(request, fill_number):
    try:
        fill = oms.get_fills(fill_number, fill_number)[0]  # TODO Update get_fill to flatten
    except IndexError:
        fill = {}
    return JsonResponse(fill)


