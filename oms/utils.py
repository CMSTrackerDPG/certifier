import logging
from django.db import IntegrityError, transaction
import runregistry
from omsapi.utilities import get_oms_run, get_oms_lumisection_count, get_oms_fill
from oms.models import OmsFill, OmsRun
from certifier.models import TrackerCertification

logger = logging.getLogger(__name__)


def get_reco_from_dataset(dataset):
    if "express" in dataset.lower():
        return "express"
    elif "prompt" in dataset.lower():
        return "prompt"
    elif "rereco" in dataset.lower() and "UL" in dataset:
        return "rerecoul"
    elif "rereco" in dataset.lower():
        return "rereco"


def retrieve_dataset_by_reco(run_number, reco):
    datasets = runregistry.get_datasets(filter={"run_number": {"=": run_number}})

    for dataset in datasets:
        if reco in dataset["name"].lower():
            return dataset["name"]

        if reco == "rereco":
            if reco in dataset["name"].lower() and "UL" not in dataset["name"]:
                return dataset["name"]

        if reco == "rerecoul":
            if "rereco" in dataset["name"].lower() and "UL" in dataset["name"]:
                return dataset["name"]

    raise Exception(f"Could not find reconstruction:{reco} for run {run_number}")


def retrieve_dataset(run_number):
    datasets = runregistry.get_datasets(filter={"run_number": {"=": run_number}})

    for dataset in datasets:
        if "online" not in dataset["name"]:
            if not TrackerCertification.objects.filter(
                runreconstruction__run__run_number=run_number,
                runreconstruction__reconstruction=get_reco_from_dataset(
                    dataset["name"]
                ),
            ).exists():
                return dataset["name"]

    if len(datasets) == 0:
        raise Exception(f"No available datasets for run {run_number}")
    raise Exception(f"Run {run_number} has been fully certified")


def retrieve_fill(fill_number):
    fill_check = OmsFill.objects.filter(fill_number=fill_number)

    if fill_check.exists():
        logger.debug(f"Fill number {fill_number} already in Database")
        return OmsFill.objects.get(fill_number=fill_number)

    # Query OMS API
    logger.debug(f"Querying OMS API for fill {fill_number}")
    response = get_oms_fill(fill_number)
    if response is None:
        logger.warning(f"Fill {fill_number} not found in OMS API")
        raise IndexError

    include_attribute_keys = [
        "fill_number",
        "b_field",
        "beta_star",
        "bunches_beam1",
        "bunches_beam2",
        "bunches_colliding",
        "bunches_target",
        "crossing_angle",
        "delivered_lumi",
        "downtime",
        "duration",
        "efficiency_lumi",
        "efficiency_time",
        "energy",
        "era",
        "fill_type_party1",
        "fill_type_party2",
        "fill_type_runtime",
        "init_lumi",
        "injection_scheme",
        "intensity_beam1",
        "intensity_beam2",
        "peak_lumi",
        "peak_pileup",
        "peak_specific_lumi",
        "recorded_lumi",
        "first_run_number",
        "last_run_number",
    ]
    include_meta_keys = [
        "init_lumi",
        "peak_lumi",
        "delivered_lumi",
        "recorded_lumi",
        "intensity_beam2",
        "intensity_beam1",
        "crossing_angle",
        "peak_specific_lumi",
        "beta_star",
    ]

    fill_kwargs = {}
    for attribute_key in include_attribute_keys:
        if attribute_key in response["attributes"].keys():
            fill_kwargs[attribute_key] = response["attributes"][attribute_key]

    for meta_key in include_meta_keys:
        meta_key_unit = meta_key + "_unit"
        if "meta" in response.keys():
            if meta_key in response["meta"]["row"].keys():
                if response["meta"]["row"][meta_key]["units"]:
                    fill_kwargs[meta_key_unit] = response["meta"]["row"][meta_key][
                        "units"
                    ]

    try:
        with transaction.atomic():
            OmsFill.objects.create(**fill_kwargs)
    except IntegrityError:
        OmsFill.objects.filter(fill_number=fill_number).update(**fill_kwargs)

    return OmsFill.objects.get(fill_number=fill_number)


def retrieve_run(run_number):
    """
    Helper function that, given a run number, tries to retrieve it
    by looking into the DB first, then the OMS API.
    If not in DB, a new entry is created and returned.
    If the API returns no results, raises an IndexError
    """
    run_check = OmsRun.objects.filter(run_number=run_number)
    if run_check.exists():
        logger.debug(f"Run {run_number} found in DB")
        return OmsRun.objects.get(run_number=run_number)

    response = get_oms_run(run_number)
    if response is None:
        logger.warning(f"Run {run_number} not found in OMS API")
        raise IndexError

    fill_number = response["attributes"].pop("fill_number")
    # There's a chance there's no fill number, see #127
    if fill_number:
        fill = retrieve_fill(fill_number=fill_number)
    else:
        fill = None

    include_attribute_keys = [
        "run_number",
        "b_field",
        "clock_type",
        "cmssw_version",
        "components",
        "delivered_lumi",
        "duration",
        "end_lumi",
        "energy",
        "fill_type_party1",
        "fill_type_party2",
        "fill_type_runtime",
        "hlt_key",
        "hlt_physics_counter",
        "hlt_physics_rate",
        "hlt_physics_size",
        "hlt_physics_throughput",
        "init_lumi",
        "initial_prescale_index",
        "l1_hlt_mode",
        "l1_hlt_mode_stripped",
        "l1_key",
        "l1_key_stripped",
        "l1_menu",
        "l1_rate",
        "l1_triggers_counter",
        "recorded_lumi",
        "sequence",
        "stable_beam",
        "tier0_transfer",
        "trigger_mode",
    ]
    include_meta_keys = ["init_lumi", "end_lumi", "delivered_lumi", "recorded_lumi"]

    run_kwargs = {}
    for attribute_key in include_attribute_keys:
        if attribute_key in response["attributes"].keys():
            run_kwargs[attribute_key] = response["attributes"][attribute_key]

    for meta_key in include_meta_keys:
        meta_key_unit = meta_key + "_unit"
        if "meta" in response.keys():
            if meta_key in response["meta"]["row"].keys():
                if response["meta"]["row"][meta_key]["units"]:
                    run_kwargs[meta_key_unit] = response["meta"]["row"][meta_key][
                        "units"
                    ]

    run_kwargs["lumisections"] = get_oms_lumisection_count(run_number)

    try:
        with transaction.atomic():
            OmsRun.objects.create(fill=fill, **run_kwargs)
    except IntegrityError as e:
        logger.warning(f"{e} trying to create OmsRun")
        OmsRun.objects.filter(run_number=run_number).update(**run_kwargs)

    return OmsRun.objects.get(run_number=run_number)
