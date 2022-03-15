import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tables.tables import SimpleRunReconstructionTable
from certifier.models import RunReconstruction, TrackerCertification
from certifier.exceptions import RunReconstructionIsAlreadyReference, RunReconstructionNotYetCertified
from oms.utils import retrieve_run
from django.contrib import messages

logger = logging.getLogger(__name__)


@login_required
def addreference(request):
    """
    Main view for listing Reference Run Reconstructions
    and adding new ones as reference or promoting existing ones.

    If user-specified Run reconstruction:
    - is not a reference and is_good, promote it
    - if it's not good, display message
    - if already a reference, inform user
    """
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)

    context = {}
    if run_number and reco:
        try:
            # Get OmsRun info from DB, create entry if does not exist
            run = retrieve_run(run_number)

            run_reconstruction, created = RunReconstruction.objects.get_or_create(
                run_id=run_number, reconstruction=reco)
            if created:
                messages.info(
                    request,
                    f"{run_reconstruction} created, must be certified first")

            try:
                run_reconstruction.promote_to_reference()
                msg = f"{run_reconstruction} has been promoted to reference"
                logger.info(msg)
                messages.success(request, msg)
            except RunReconstructionIsAlreadyReference:
                msg = f"{run_reconstruction} already a reference"
                logger.debug(msg)
                messages.info(request, msg)
            except RunReconstructionNotYetCertified:
                msg = f"{run_reconstruction} has not been certified yet!"
                logger.warning(msg)
                messages.warning(request, msg)

        except IndexError:
            context = {"message": f"Run {run_number} does not exist"}
            return render(request, "certifier/404.html", context)

    # Get all reference runreconstructions and render them
    run_info_list = RunReconstruction.objects.filter(is_reference=True)
    table = SimpleRunReconstructionTable(run_info_list)

    context["table"] = table
    context["run_number"] = run_number
    context["reco"] = reco

    return render(request, "addrefrun/addrefrun.html", context)
