from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from certifier.models import TrackerCertification, RunReconstruction, Dataset, BadReason
# Create your views here.
from django.shortcuts import redirect
from oms.utils import retrieve_run, retrieve_dataset, get_reco_from_dataset
from .forms import CertifyFormWithChecklistForm, DatasetForm, BadReasonForm
from oms.models import OmsRun
from users.models import User
from django.http import HttpResponseRedirect

@login_required #WIP
def addBadReason(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BadReasonForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            try:
                name = BadReason.objects.get(
                        name=request.POST.get("name"))
            except BadReason.DoesNotExist:
                form.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = BadReasonForm()

    return render(request, "certifier/badreason.html", {"form": form})

@login_required #WIP
def createDataset(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DatasetForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            try:
                dataset = Dataset.objects.get(
                        dataset=request.POST.get("dataset"))
            except Dataset.DoesNotExist:
                form.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = DatasetForm()

    return render(request, "certifier/dataset.html", {"form": form})

@login_required
def certify(request, run_number):
    try:
        run = retrieve_run(run_number)
        dataset = retrieve_dataset(run_number)
    except IndexError or ConnectionError:
        context = {"message": "Run {} does not exist".format(run_number)}
        return render(request, "certifier/404.html", context)

    reco = get_reco_from_dataset(dataset)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        try:
            runReconstruction = RunReconstruction.objects.get(
                    run__run_number=run_number,reconstruction=reco)
        except RunReconstruction.DoesNotExist:
            runReconstruction = RunReconstruction.objects.create(
                    run=run, reconstruction=reco)

        try:
            dataset = Dataset.objects.get(dataset=dataset)
        except Dataset.DoesNotExist:
            dataset = Dataset.objects.create(dataset=dataset)

        user = User.objects.get(pk=request.user.id)

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
                formToSave.dataset = dataset
                formToSave.user=user
                formToSave.save()
                form.save_m2m()

            return redirect("listruns:list")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CertifyFormWithChecklistForm()

    context = {"run_number": run_number, "reco": reco, "run": run, "dataset": dataset, "form": form}

    return render(request, "certifier/certify.html", context)
