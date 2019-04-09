from django.shortcuts import render
from certifier.models import TrackerCertification, RunReconstruction
# Create your views here.
from django.shortcuts import redirect
from oms.utils import retrieve_run
from .forms import CertifyFormWithChecklistForm
from oms.models import OmsRun
from users.models import User

def index(request):
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)

    from django.shortcuts import redirect

    if run_number and reco:
        response = redirect("/certify/{}/{}".format(run_number, reco))
        return response

    return render(request, "certifier/index.html")

def listruns(request):
    data = TrackerCertification.objects.all()
    context = {
        "objs": data
    }
    return render(request, "certifier/test.html",context)


def certify(request, run_number, reco):
    try:
        run = retrieve_run(run_number)
    except IndexError:
        context = {"message": "Run {} does not exist".format(run_number)}
        return render(request, "certifier/404.html", context)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        try:
            runReconstruction = RunReconstruction.objects.get(
                    run__run_number=run_number,reconstruction=reco)
        except RunReconstruction.DoesNotExist:
            runReconstruction = RunReconstruction.objects.create(
                    run=run, reconstruction=reco, dataset="test")

        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            user = None

        # create a form instance and populate it with data from the request:
        form = CertifyFormWithChecklistForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            try:
                trackerCertification = TrackerCertification.objects.get(runreconstruction=runReconstruction)
            except TrackerCertification.DoesNotExist:
                formToSave = form.save(commit=False)
                formToSave.runreconstruction=runReconstruction
#                formToSave.user=user
                formToSave.save()

            return redirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CertifyFormWithChecklistForm()

    context = {"run_number": run_number, "reco": reco, "run": run, "form": form}

    return render(request, "certifier/certify.html", context)
