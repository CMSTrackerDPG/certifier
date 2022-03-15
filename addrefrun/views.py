import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tables.tables import SimpleRunReconstructionTable
from certifier.models import RunReconstruction, TrackerCertification
from oms.utils import retrieve_run
from django.contrib import messages

logger = logging.getLogger(__name__)


@login_required
def addreference(request):
    """
    Main view for listing Reference Run Reconstructions. 
    If specified Run reconstruction:
    - is not a reference and is_good, promote it
    - if it's not good, display message
    - if already a reference, inform user
    """
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)
    if run_number and reco:
        logger.debug(f"Requested to make {run_number} ({reco}) a reference")

    # add_reference_failed = False

    context = {}

    if run_number and reco:
        try:
            # Get OmsRun info from DB, create entry if does not exist
            run = retrieve_run(run_number)

            # if not RunReconstruction.objects.filter(
            #         run__run_number=run_number, reconstruction=reco).exists():
            #     runReconstruction = RunReconstruction.objects.create(
            #         run=run, reconstruction=reco, is_reference=True)
            # else:
            #     add_reference_failed = True
            run_reconstruction, created = RunReconstruction.objects.get_or_create(
                run_id=run_number, reconstruction=reco)

            if not run_reconstruction.is_reference:
                # Look into TrakcerCertification for the specific run reconstruction
                # to see if it has been certified. RunReconstruction ids are TrackerCertification's
                # primary key
                if TrackerCertification.objects.filter(
                        runreconstruction=run_reconstruction).exists(
                        ) and run_reconstruction.certification.is_good:
                    # Run reconstruction has been certified and is good,
                    # so we're promoting it. This code should, perhaps, be shared
                    # with the promote view in shiftleader
                    run_reconstruction.is_reference = True
                    run_reconstruction.save()
                    msg = f"{run_number} ({reco}) has been promoted to reference"
                    logger.info(msg)
                    messages.success(request, msg)
                else:
                    msg = f"{run_number} ({reco}) has not been certified yet!"
                    messages.warning(request, msg)
                    # add_reference_failed = True
            else:
                msg = f"{run_number} ({reco}) already a reference"
                messages.info(request, msg)
                logger.debug(msg)
        except IndexError:
            context = {"message": f"Run {run_number} does not exist"}
            return render(request, "certifier/404.html", context)

    # Get all reference runreconstructions and render them
    run_info_list = RunReconstruction.objects.filter(is_reference=True)
    table = SimpleRunReconstructionTable(run_info_list)

    # Warning message, should only appear on error when adding a
    # runreconstruction as reference
    context["table"] = table
    # context["add_reference_failed"] = add_reference_failed
    context["run_number"] = run_number
    context["reco"] = reco

    return render(request, "addrefrun/addrefrun.html", context)
