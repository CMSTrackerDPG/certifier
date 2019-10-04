from django.shortcuts import render
from django.views import generic
from certifier.models import TrackerCertification, RunReconstruction
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from certifier.forms import CertifyForm
from openruns.models import OpenRuns

# Create your views here.
@method_decorator(login_required, name="dispatch")
class DeleteRun(generic.DeleteView):
    """
    Deletes a specific Run from the TrackerCertification table
    """

    model = TrackerCertification
    form_class = CertifyForm
    success_url = "/shiftleader/"
    template_name = "delete/trackercertification_delete_form.html"

@login_required
def hard_delete_run_view(request, pk, run_number, reco):
    try:
        trackerCertification = TrackerCertification.all_objects.get(pk=pk)
    except TrackerCertification.DoesNotExist:
        raise Http404("The run with the id {} doesnt exist".format(pk))

    if request.method == "POST":
        trackerCertification.hard_delete()
        return HttpResponseRedirect("/shiftleader/")

    return render(request, "delete/hard_delete.html", {"trackerCertification": trackerCertification})


@login_required
def hard_delete_reference_run(request, run_number, reco):
    try:
        runReconstruction = RunReconstruction.objects.get(run__run_number=run_number, reconstruction=reco, is_reference=True)
    except RunReconstruction.DoesNotExist:
        raise Http404("The run  {} doesnt exist".format(run_number))

    if request.method == "POST":
        runReconstruction.delete()
        return HttpResponseRedirect("/reference/")

    return render(request, "delete/hard_delete_reference_run.html", {"runReconstruction": runReconstruction})

@login_required
def hard_delete_open_run(request, run_number):
    try:
        openrun = OpenRuns.objects.get(run_number=run_number)
    except OpenRuns.DoesNotExist:
        raise Http404("The run  {} doesnt exist".format(run_number))

    openrun.delete()
    return HttpResponseRedirect("/openruns/")
