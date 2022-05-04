import logging
import json
from xml.etree.ElementTree import ParseError
from requests.exceptions import SSLError, ConnectionError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, Http404, JsonResponse
from certifier.forms import CertifyFormWithChecklistForm, BadReasonForm
from certifier.models import TrackerCertification, RunReconstruction, Dataset, BadReason
from certifier.api.serializers import RunReferenceRunSerializer
from openruns.models import OpenRuns
from oms.utils import (
    retrieve_run,
    retrieve_dataset,
    retrieve_dataset_by_reco,
    get_reco_from_dataset,
)
from oms.models import OmsRun
from users.models import User

logger = logging.getLogger(__name__)


@login_required
def badReason(request):
    """
    View for getting and adding Bad reasons
    for certification
    """
    response = {}
    # Add bad reason
    if (
        request.method
        == "POST"
        # and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    ):
        name = request.POST.get("name", None)
        description = request.POST.get("description", None)

        if name and description:
            try:
                BadReason.objects.get(name=name)
            except BadReason.DoesNotExist:
                BadReason.objects.create(name=name, description=description)

    response["bad_reasons"] = list(BadReason.objects.all().values())

    return JsonResponse(response)


@login_required
def addBadReasonForm(request):
    """
    View which makes available a BadReasonForm.
    Used by the certify view to load the form via jQuery.load().
    """
    form = BadReasonForm()

    return render(request, "certifier/badreason.html", {"form": form})


@login_required
def promoteToReference(request, run_number, reco):
    """
    View which is called from the Shift Leader View, to promote a specific run
    reconstruction to a reference one.
    """
    try:
        runReconstruction = RunReconstruction.objects.get(
            run__run_number=run_number, reconstruction=reco
        )
    except RunReconstruction.DoesNotExist as run_reco_does_not_exist:
        raise Http404(
            f"The run {run_number} doesn't exist"
        ) from run_reco_does_not_exist

    if request.method == "POST":
        runReconstruction.promote_to_reference()
        return HttpResponseRedirect("/shiftleader/")

    return render(
        request, "certifier/promote.html", {"runReconstruction": runReconstruction}
    )


@login_required
def certify(request, run_number, reco=None):

    logger.debug(f"Requesting certification of run {run_number} {reco if reco else ''}")

    # Check if specific combination can be certified by current user
    if not TrackerCertification.can_be_certified_by_user(
        run_number, reco, request.user
    ):
        msg = f"Reconstruction {run_number} {reco} is already certified by another user"
        logger.warning(msg)
        return render(
            request,
            "certifier/http_error.html",
            context={"error_num": 400, "message": msg},
            status=400,
        )
    # If certification exists, redirect to update it
    elif TrackerCertification.objects.filter(
        runreconstruction__run__run_number=run_number,
        runreconstruction__reconstruction=reco,
    ).exists():
        certification = TrackerCertification.objects.get(
            runreconstruction__run__run_number=run_number,
            runreconstruction__reconstruction=reco,
        )
        return redirect(
            "listruns:update", pk=certification.pk, run_number=run_number, reco=reco
        )

    # This is only available from openruns colored boxes
    dataset = request.GET.get("dataset", None)

    run = None
    try:
        run = retrieve_run(run_number)
        if not dataset:
            if not reco:
                dataset = retrieve_dataset(run_number)
            else:
                dataset = retrieve_dataset_by_reco(run_number, reco)

    except IndexError as e:
        context = {"message": f"Run {run_number} does not exist"}
        logger.error(f"{context['message']} ({repr(e)})")
        return render(request, "certifier/404.html", context, status=404)
    except (
        ConnectionError,
        ParseError,
    ) as e:
        if isinstance(e, ConnectionError):
            msg = "Unable to connect to external API."
        elif isinstance(e, ParseError):
            msg = "CERN authentication failed."
        msg += f" Please proceed to enter the data manually (Error: {e})"
        logger.warning(msg)

        # If no reconstruction is specified and there's no connection
        # to RR, we cannot get the next available reconstruction type & dataset
        if not reco:
            context = {
                "message": f"Cannot proceed with certification if no reconstuction type is specified ({e})",
                "error_num": 400,
            }
            return render(request, "certifier/http_error.html", context, status=400)
        # Proceed with warning
        messages.warning(request, msg)

    except Exception as e:
        context = {"message": e, "error_num": 500}
        logger.exception(repr(e))
        return render(request, "certifier/http_error.html", context, status=500)

    if not reco:
        if dataset:
            reco = get_reco_from_dataset(dataset)
        else:
            reco = None

    # Certification submission
    if request.method == "POST":

        try:
            runReconstruction = RunReconstruction.objects.get(
                run__run_number=run_number, reconstruction=reco
            )
        except RunReconstruction.DoesNotExist:
            runReconstruction = RunReconstruction.objects.create(
                run=run, reconstruction=reco
            )

        dataset, _ = Dataset.objects.get_or_create(dataset=dataset)

        user = User.objects.get(pk=request.user.id)

        # create a form instance and populate it with data from the request:
        form = CertifyFormWithChecklistForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            try:
                trackerCertification = TrackerCertification.objects.get(
                    runreconstruction=runReconstruction
                )
                messages.warning(
                    request,
                    f"Certification for {trackerCertification.runreconstruction.run.run_number} {trackerCertification.runreconstruction.reconstruction} already exists",
                )
            except TrackerCertification.DoesNotExist:
                formToSave = form.save(commit=False)
                formToSave.runreconstruction = runReconstruction
                formToSave.dataset = dataset
                formToSave.user = user
                formToSave.save()
                form.save_m2m()
                messages.info(
                    request,
                    f"Certification for {runReconstruction.run.run_number} {runReconstruction.reconstruction} successfully saved",
                )
            return redirect("openruns:openruns")

        messages.error(request, "Submitted form was invalid!")

    # From openruns openruns page, create a blank form
    elif request.method == "GET":
        form = CertifyFormWithChecklistForm()

    context = {
        "run_number": run_number,
        "reco": reco,
        "run": run,
        "dataset": dataset,
        "form": form,
    }

    return render(request, "certifier/certify.html", context)


def runRefRun_list(request):
    """
    Simple list view of serialized Reference runs

    Transferred from old 'mldatasets' app
    """
    if request.method == "GET":
        runRefRunsAll = TrackerCertification.objects.all()
        serializer = RunReferenceRunSerializer(runRefRunsAll, many=True)
        return JsonResponse(serializer.data, safe=False)
