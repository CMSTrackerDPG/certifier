import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import JsonResponse
from django.shortcuts import render
from tables.tables import ReferenceRunReconstructionTable
from certifier.models import RunReconstruction, TrackerCertification
from certifier.exceptions import (
    RunReconstructionIsAlreadyReference,
    RunReconstructionNotYetCertified,
)
from oms.utils import oms_retrieve_run
from django.contrib import messages

logger = logging.getLogger(__name__)


@user_passes_test(
    lambda user: hasattr(user, "has_shift_leader_rights")
    and user.has_shift_leader_rights,
    redirect_field_name=None,
)
def addreference(request):  # pragma: no cover
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
            run = oms_retrieve_run(run_number)

            run_reconstruction, created = RunReconstruction.objects.get_or_create(
                run_id=run_number, reconstruction=reco
            )
            if created:
                messages.info(
                    request, f"{run_reconstruction} created, must be certified first"
                )

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
    table = ReferenceRunReconstructionTable(run_info_list)

    context["table"] = table
    context["run_number"] = run_number
    context["reco"] = reco

    return render(request, "addrefrun/addrefrun.html", context)


@user_passes_test(
    lambda user: hasattr(user, "has_shift_leader_rights")
    and user.has_shift_leader_rights,
    redirect_field_name=None,
)
def update_refruns_info(request):
    """
    View which triggers an update of the Runs associated with
    all reference reconstructions.

    This is done on demand, because the web app required to
    acquire the APV mode information is slow.
    """
    success = False
    ref_run_recos = RunReconstruction.objects.filter(is_reference=True)
    try:
        for rrr in ref_run_recos:
            rrr.run.update_apv_mode()
            rrr.run.save()
        success = True
    except Exception as e:
        logger.error(e)

    return JsonResponse({"success": success})
