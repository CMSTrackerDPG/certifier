from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tables.tables import SimpleRunReconstructionTable
from certifier.models import RunReconstruction
from oms.utils import retrieve_run
from django.contrib import messages

# Create your views here.
@login_required
def addreference(request):
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)
    add_reference_failed = False

    context = {}

    messages.info(request, 'Your password has been changed successfully!')

    if run_number and reco:
        try:
            run = retrieve_run(run_number)

            if not RunReconstruction.objects.filter(run__run_number=run_number,reconstruction=reco).exists():
                runReconstruction = RunReconstruction.objects.create(run=run, reconstruction=reco, is_reference=True)
            else:
                add_reference_failed = True
        except IndexError:
            context = {"message": "Run {} does not exist".format(run_number)}
            return render(request, "certifier/404.html", context)


    run_info_list = RunReconstruction.objects.filter(is_reference=True)
    table = SimpleRunReconstructionTable(run_info_list)

    context["table"] = table
    context["add_reference_failed"] = add_reference_failed
    context["run_number"] = run_number
    context["reco"] = reco

    return render(request, "addrefrun/addrefrun.html", context)
