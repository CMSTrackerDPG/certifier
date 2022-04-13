import logging
import runregistry
from django.utils import timezone
from openruns.models import OpenRuns

logger = logging.getLogger(__name__)


def get_specific_open_runs(runs_list, user):
    logger.info(f"Getting all OPEN RR datasets for run numbers {runs_list}")
    datasets = runregistry.get_datasets(
        filter={
            "run_number": {
                "or": runs_list
            },
            "dataset_name": {
                "and": [{
                    "<>": "online"
                }]
            },
            # "tracker_state": {
            #     "=": "OPEN"
            # }
        })
    logger.info(f"Got {len(datasets)} datasets.")
    get_datasets_of_runs(datasets, user)


def get_range_of_open_runs(start, end, user):
    logger.info(f"Getting all OPEN RR datasets for runs {start} to {end}")
    datasets = runregistry.get_datasets(
        filter={
            "run_number": {
                "and": [{
                    ">=": start
                }, {
                    "<=": end
                }]
            },
            "dataset_name": {
                "and": [{
                    "<>": "online"
                }]
            },
            # "tracker_state": {
            #     "=": "OPEN"
            # }
        })
    logger.info(f"Got {len(datasets)} datasets.")

    get_datasets_of_runs(datasets, user)


def get_datasets_of_runs(datasets, user):
    """
    Given a list of RunRegistry datasets, for each one:
    - Creates an OpenRuns object
    """
    today = timezone.now().strftime("%Y-%m-%d")

    for dataset in datasets:
        run_number = dataset["run_number"]
        logger.debug(f"Dataset {run_number}: {dataset['name']}")
        run_check = OpenRuns.objects.filter(run_number=run_number)

        dataset_express = ""
        dataset_prompt = ""
        dataset_rereco = ""
        dataset_rereco_ul = ""
        state_express = ""
        state_prompt = ""
        state_rereco = ""
        state_rereco_ul = ""

        # Depending on the reconstruction type, update the
        # OpenRuns entry with the dataset name, if does not exist
        if "express" in dataset["name"].lower():
            dataset_express = dataset["name"]
            state_express = (dataset["dataset_attributes"]["tracker_state"]
                             if "tracker_state"
                             in dataset["dataset_attributes"] else "SIGNOFF")
            run_dataset_check = OpenRuns.objects.filter(
                run_number=run_number).filter(dataset_express=dataset_express)
            if not run_dataset_check.exists() and run_check.exists():
                run_check.update(
                    dataset_express=dataset_express,
                    state_express=state_express)  # Date is updated at the end

        elif "prompt" in dataset["name"].lower():
            dataset_prompt = dataset["name"]
            state_prompt = (dataset["dataset_attributes"]["tracker_state"]
                            if "tracker_state" in dataset["dataset_attributes"]
                            else "SIGNOFF")
            run_dataset_check = OpenRuns.objects.filter(
                run_number=run_number).filter(dataset_prompt=dataset_prompt)
            if not run_dataset_check.exists() and run_check.exists():
                run_check.update(dataset_prompt=dataset_prompt,
                                 state_prompt=state_prompt)

        elif "rereco" in dataset["name"].lower() and "UL" in dataset["name"]:
            dataset_rereco_ul = dataset["name"]
            state_rereco_ul = (dataset["dataset_attributes"]["tracker_state"]
                               if "tracker_state"
                               in dataset["dataset_attributes"] else "SIGNOFF")
            run_dataset_check = OpenRuns.objects.filter(
                run_number=run_number).filter(dataset_rereco=dataset_rereco)
            if not run_dataset_check.exists() and run_check.exists():
                run_check.update(dataset_rereco_ul=dataset_rereco_ul,
                                 state_rereco_ul=state_rereco_ul)

        elif "rereco" in dataset["name"].lower():
            dataset_rereco = dataset["name"]
            state_rereco = (dataset["dataset_attributes"]["tracker_state"]
                            if "tracker_state" in dataset["dataset_attributes"]
                            else "SIGNOFF")
            run_dataset_check = OpenRuns.objects.filter(
                run_number=run_number).filter(
                    dataset_rereco_ul=dataset_rereco_ul)
            if not run_dataset_check.exists() and run_check.exists():
                run_check.update(dataset_rereco=dataset_rereco,
                                 state_rereco=state_rereco)

        # In case the OpenRuns entry does not exist yet, create it
        if not run_dataset_check.exists() and not run_check.exists():
            if (dataset_express != "" or dataset_prompt != ""
                    or dataset_rereco != "" or dataset_rereco_ul != ""):
                OpenRuns.objects.create(
                    run_number=dataset["run_number"],
                    # user=user,
                    dataset_express=dataset_express,
                    dataset_prompt=dataset_prompt,
                    dataset_rereco=dataset_rereco,
                    dataset_rereco_ul=dataset_rereco_ul,
                    state_express=state_express,
                    state_prompt=state_prompt,
                    state_rereco=state_rereco,
                    state_rereco_ul=state_rereco_ul,
                    date_retrieved=today,
                )
        else:
            run_check.update(date_retrieved=today)
