from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from certifier.models import TrackerCertification, RunReconstruction, Dataset, BadReason
# Create your views here.
from django.shortcuts import redirect
from oms.utils import retrieve_run, retrieve_dataset, retrieve_dataset_by_reco, get_reco_from_dataset
from .forms import CertifyFormWithChecklistForm, DatasetForm, BadReasonForm
from oms.models import OmsRun
from users.models import User
from django.http import HttpResponseRedirect, Http404

@login_required
def addBadReason(request):
    # if this is a POST request we need to process the form data
    form = BadReasonForm()

    return render(request, "certifier/badreason.html", {"form": form})

@login_required
def promoteToReference(request, run_number, reco):
    try:
        runReconstruction = RunReconstruction.objects.get(run__run_number=run_number, reconstruction=reco)
    except RunReconstruction.DoesNotExist:
        raise Http404("The run  {} doesnt exist".format(run_number))

    if request.method == "POST":
        runReconstruction.is_reference = True
        runReconstruction.save()
        return HttpResponseRedirect("/shiftleader/")

    return render(request, "certifier/promote.html", {"runReconstruction": runReconstruction})

@login_required
def certify(request, run_number, reco=None):
    
    print(request)
    
    if request.is_ajax():
        name = request.POST.get("name", None)
        dataset = request.POST.get("dataset", None)
        description = request.POST.get("description", None)
        run = OmsRun.objects.get(run_number=run_number)

        if name and description and dataset:

            try:
                BadReason.objects.get(name=name)
            except BadReason.DoesNotExist:
                BadReason.objects.create(name=name, description=description)

            form = CertifyFormWithChecklistForm()

            context = {"run_number": run_number, "reco": reco, "run": run, "dataset": dataset, "form": form}

            return render(request, "certifier/certify.html", context)

    dataset = request.GET.get('dataset',None)

    try:
        
        run = retrieve_run(run_number)

        if not dataset:
            if not reco:
                dataset = retrieve_dataset(run_number)
            else:
                dataset = retrieve_dataset_by_reco(run_number, reco)
        else:
            dataset=dataset
    
        print(request)
    except (IndexError, ConnectionError) as e:
        context = {"message": "Run {} does not exist".format(run_number)}
        return render(request, "certifier/404.html", context)
    except Exception as e:
        context = {"message": e}
        return render(request, "certifier/404.html", context)

    if not reco:
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

            return redirect("openruns:openruns")

    # if a GET (or any other method) we'll create a blank form
    if request.method == "GET":
        form = CertifyFormWithChecklistForm()

    context = {"run_number": run_number, "reco": reco, "run": run, "dataset": dataset, "form": form}

    return render(request, "certifier/certify.html", context)
