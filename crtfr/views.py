from django.shortcuts import render
from django.http import Http404


# Create your views here.
from wbmcrawlr import oms

from utils.omsutils import retrieve_run


def index(request):
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)

    from django.shortcuts import redirect

    if run_number and reco:
        response = redirect("/certify/{}/{}".format(run_number, reco))
        return response

    return render(request, "crtfr/index.html")


def certify(request, run_number, reco):
    try:
        run = retrieve_run(run_number)
    except IndexError:
        context = {"message": "Run {} does not exist".format(run_number)}
        return render(request, "crtfr/404.html", context)

    context = {"run_number": run_number, "reco": reco, "run": run}
    return render(request, "crtfr/certify.html", context)


def analyse(request, run_number, reco):
    run = retrieve_run(run_number)
    context = {"run_number": run_number, "reco": reco, "run": run}
    return render(request, "crtfr/analyse.html", context)


def plot(request, run_number, reco):
    run = retrieve_run(run_number)
    context = {"run_number": run_number, "reco": reco, "run": run}
    return render(request, "crtfr/plot.html", context)
