from django.shortcuts import render
from django.views import generic
from certifier.models import TrackerCertification
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from certifier.forms import CertifyForm

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

