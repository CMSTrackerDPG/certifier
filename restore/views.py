from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from certifier.models import TrackerCertification
from django.http import HttpResponseRedirect, Http404

# Create your views here.

@login_required
def restore_run_view(request, pk, run_number, reco):
    try:
        trackerCertification = TrackerCertification.all_objects.get(pk=pk)
    except TrackerCertification.DoesNotExist:
        raise Http404("The run with the id {} doesnt exist".format(pk))

    if request.method == "POST":
        trackerCertification.restore()
        return HttpResponseRedirect("/shiftleader/")

    return render(request, "restore/restore.html", {"trackerCertification": trackerCertification})
