from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tables.tables import SimpleRunReconstructionTable
from certifier.models import RunReconstruction
from oms.utils import retrieve_run

# Create your views here.
@login_required
def addreference(request):
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)

    context = {}

    if run_number and reco:
        try:
            run = retrieve_run(run_number)

            try:
                runReconstruction = RunReconstruction.objects.get(run__run_number=run_number,reconstruction=reco, is_reference=True)
            except RunReconstruction.DoesNotExist:
                runReconstruction = RunReconstruction.objects.create(run=run, reconstruction=reco, is_reference=True)
        except IndexError:
            context = {"message": "Run {} does not exist".format(run_number)}
            return render(request, "certifier/404.html", context)


    try:
        run_info_list = RunReconstruction.objects.filter(is_reference=True)
        print(run_info_list)
        table = SimpleRunReconstructionTable(run_info_list)
    except RunReconstruction.DoesNotExist:
        print("nimic")
        table = SimpleRunReconstructionTable([])

    context["table"] = table

    return render(request, "addrefrun/addrefrun.html", context)
