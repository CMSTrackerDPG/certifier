import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tables.tables import SimpleRunReconstructionTable
from certifier.models import RunReconstruction
from oms.utils import retrieve_run
# from django.contrib import messages

logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def addreference(request):
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)
    logger.debug(f"Requested to add {run_number} ({reco}) as reference")
    add_reference_failed = False

    context = {}

    # No idea why this is here, commented it out
    # messages.info(request, 'Your password has been changed successfully!')

    if run_number and reco:
        try:
            # Get OmsRun info from DB, create entry if does not exist
            run = retrieve_run(run_number)

            if not RunReconstruction.objects.filter(
                    run__run_number=run_number, reconstruction=reco).exists():
                runReconstruction = RunReconstruction.objects.create(
                    run=run, reconstruction=reco, is_reference=True)
            else:
                add_reference_failed = True
        except IndexError:
            context = {"message": f"Run {run_number} does not exist"}
            return render(request, "certifier/404.html", context)

    # Get all reference runreconstructions and render them
    run_info_list = RunReconstruction.objects.filter(is_reference=True)
    table = SimpleRunReconstructionTable(run_info_list)

    # Warning message, should only appear on error when adding a
    # runreconstruction as reference
    context["table"] = table
    context["add_reference_failed"] = add_reference_failed
    context["run_number"] = run_number
    context["reco"] = reco

    return render(request, "addrefrun/addrefrun.html", context)
