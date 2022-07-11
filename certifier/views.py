import logging
import json
from xml.etree.ElementTree import ParseError
from requests.exceptions import SSLError, ConnectionError
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, Http404, JsonResponse
from certifier.forms import CertifyFormWithChecklistForm, BadReasonForm
from certifier.models import TrackerCertification, RunReconstruction, Dataset, BadReason
from certifier.api.serializers import RunReferenceRunSerializer
from certifier.exceptions import RunReconstructionAllDatasetsCertified
from openruns.models import OpenRuns
from oms.utils import (
    oms_retrieve_run,
    rr_retrieve_next_uncertified_dataset,
    rr_retrieve_dataset_by_reco,
    get_reco_from_dataset,
)
from oms.models import OmsRun, OmsFill
from oms.exceptions import (
    OmsApiFillNumberNotFound,
    OmsApiRunNumberNotFound,
    RunRegistryNoAvailableDatasets,
    RunRegistryReconstructionNotFound,
)
from oms.views import OmsRunUpdateView, OmsFillUpdateView
from oms.forms import OmsRunForm, OmsFillForm
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


@method_decorator(login_required, name="dispatch")
class CertifyView(View):
    form = CertifyFormWithChecklistForm
    run = None
    reco = None
    dataset = None
    external_info_complete = False
    _rr_info_updated = False
    _oms_info_updated = False

    def dispatch(self, request, *args, **kwargs):
        """
        Override parent class' dispatch method (i.e. before get() or post()
        is executed) to make sure we have enough info to proceed

        Notes:
        - We always have run_number available
        - Having the dataset, we easily have reco too
        - Having just run_number but not the dataset means
        try to find the next available dataset from RR
        """
        run_number = kwargs.get("run_number", None)
        self.reco = kwargs.get("reco", None)
        self.dataset = request.GET.get("dataset", None)

        # Make sure that we have the dataset name and the reconstruction type
        try:
            if not self.dataset and not self.reco:
                self.dataset = rr_retrieve_next_uncertified_dataset(run_number)
                self.reco = get_reco_from_dataset(self.dataset)
            elif not self.dataset:
                self.dataset = rr_retrieve_dataset_by_reco(run_number, self.reco)
            elif not self.reco:
                self.reco = get_reco_from_dataset(self.dataset)
            self._rr_info_updated = True
        except RunReconstructionAllDatasetsCertified as e:
            logger.info(repr(e))
            messages.success(request, repr(e))
            return redirect("openruns:openruns")
        except (
            ConnectionError,
            ParseError,
            RunRegistryReconstructionNotFound,
            RunRegistryNoAvailableDatasets,
        ) as e:
            # If no reconstruction is specified and there's no connection
            # to RR, we cannot get the next available reconstruction type & dataset
            if not self.reco:
                context = {
                    "message": "Cannot proceed with certification if no "
                    f"reconstruction type is specified first ({e})",
                    "error_num": 400,
                }
                return render(request, "certifier/http_error.html", context, status=400)

            # Proceed with warning
            if isinstance(e, ConnectionError):
                msg = "Unable to connect to external API."
            elif isinstance(e, ParseError):
                msg = "CERN authentication failed."
            else:
                msg = ""
            msg += f" Please proceed to enter the data manually (Error: {e})"
            logger.warning(msg)
            messages.warning(request, msg)

        # Check if specific combination can be certified by current user
        if not TrackerCertification.can_be_certified_by_user(
            run_number, self.reco, request.user
        ):
            msg = (
                f"Reconstruction {run_number} {self.reco} "
                "is already certified by another user"
            )
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
            runreconstruction__reconstruction=self.reco,
        ).exists():
            certification = TrackerCertification.objects.get(
                runreconstruction__run__run_number=run_number,
                runreconstruction__reconstruction=self.reco,
            )

            return redirect(
                "listruns:update",
                pk=certification.pk,
                run_number=run_number,
                reco=self.reco,
            )

        try:
            # This does not raise if run was created
            # previously, even without remote information
            self.run = oms_retrieve_run(run_number)
            self._oms_info_updated = True
        except (
            ConnectionError,
            ParseError,
            OmsApiRunNumberNotFound,
            OmsApiFillNumberNotFound,
        ) as e:
            # If OMS API does not contain the info required,
            # or OMS is unreachable, create the run with minimal
            # info
            messages.warning(request, repr(e))
            self.run, _ = OmsRun.objects.get_or_create(run_number=run_number)

        # Update flag
        self.external_info_complete = self._rr_info_updated and self._oms_info_updated

        logger.debug(f"Run reconstruction {run_number} {self.reco} ({self.dataset})")
        # All good, proceed with dispatching to the appropriate method
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, run_number: int, reco: str = None):
        logger.debug(
            f"Requesting certification of run {run_number} {reco if reco else ''}"
        )
        self.run.run_type = OmsRun.COLLISIONS

        context = {
            "run_number": run_number,
            "reco": self.reco,
            "run": self.run,
            "dataset": self.dataset,
            "form": self.form(
                initial={"external_info_complete": self.external_info_complete}
            ),
            "omsrun_form": OmsRunForm(instance=self.run),
            "omsfill_form": OmsFillForm(
                instance=self.run.fill if self.run.fill else None
            ),
        }
        return render(request, "certifier/certify.html", context)

    def post(self, request, run_number: int, reco: str = None):
        logger.debug(f"Submitting certification for run {run_number} {self.reco}")
        try:
            runReconstruction = RunReconstruction.objects.get(
                run__run_number=run_number, reconstruction=self.reco
            )
        except RunReconstruction.DoesNotExist:
            runReconstruction = RunReconstruction.objects.create(
                run=self.run, reconstruction=self.reco
            )

        dataset = None
        if self.dataset:
            dataset, _ = Dataset.objects.get_or_create(dataset=self.dataset)

        user = User.objects.get(pk=request.user.id)

        omsfill_form = OmsFillForm(request.POST)

        # If manually editing form
        if not request.POST.get("external_info_complete"):
            fill = None
            if OmsFill.objects.filter(
                fill_number=omsfill_form.data["fill_number"]
            ).exists():
                omsfill_form = OmsFillForm(
                    request.POST,
                    instance=OmsFill.objects.get(
                        fill_number=omsfill_form.data["fill_number"]
                    ),
                )
            elif not omsfill_form.is_valid():
                msg = f"OmsFill form has errors! {dict(omsfill_form.errors)}"
                logger.error(msg)
                messages.error(request, msg)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            fill = omsfill_form.save()

            omsrun_form = OmsRunForm(request.POST, instance=self.run)
            if omsrun_form.is_valid():
                self.run = omsrun_form.save(commit=False)
                self.run.fill = fill
                self.run.save()

            else:
                msg = f"OmsRun form has errors! {dict(omsrun_form.errors)}"
                logger.error(msg)
                messages.error(request, msg)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        # create a form instance and populate it with data from the request:
        form = self.form(request.POST)

        if form.is_valid():
            try:
                trackerCertification = TrackerCertification.objects.get(
                    runreconstruction=runReconstruction
                )
                messages.info(
                    request,
                    f"Certification for {trackerCertification.runreconstruction.run.run_number} "
                    f"{trackerCertification.runreconstruction.reconstruction} already exists",
                )
            except TrackerCertification.DoesNotExist:
                formToSave = form.save(commit=False)
                formToSave.runreconstruction = runReconstruction
                formToSave.dataset = dataset
                formToSave.user = user
                formToSave.save()
                form.save_m2m()
                messages.success(
                    request,
                    f"Certification for {runReconstruction.run.run_number} "
                    f"{runReconstruction.reconstruction} successfully saved",
                )
        else:
            messages.error(
                request, f"Submitted form was invalid! ({dict(form.errors)})"
            )

        return redirect("openruns:openruns")


def runRefRun_list(request):
    """
    Simple list view of serialized Reference runs

    Transferred from old 'mldatasets' app
    """
    if request.method == "GET":
        runRefRunsAll = TrackerCertification.objects.all()
        serializer = RunReferenceRunSerializer(runRefRunsAll, many=True)
        return JsonResponse(serializer.data, safe=False)
