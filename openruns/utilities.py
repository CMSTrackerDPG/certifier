from typing import List, Dict
import logging
import runregistry
from django.utils import timezone
from openruns.models import OpenRuns

logger = logging.getLogger(__name__)


def get_specific_open_runs(runs_list: List[int]) -> None:
    """
    Function that gets a list of run numbers, queries RR for them,
    gets the available datasets for these runs and calls get_datasets_of_runs
    """
    logger.info(f"Getting all OPEN RR datasets for run numbers {runs_list}")
    datasets = runregistry.get_datasets(filter={
        "run_number": {
            "or": runs_list
        },
        "tracker_state": {
            "=": "OPEN"
        }
    })
    logger.info(f"Got {len(datasets)} datasets.")
    get_datasets_of_runs(datasets)


def get_range_of_open_runs(start: int, end: int) -> None:
    """
    Function that gets a range of run numbers and queries RR for 
    the available OPEN datasets for those runs.
    """
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
            "tracker_state": {
                "=": "OPEN"
            },
        })
    logger.info(f"Got {len(datasets)} datasets.")

    get_datasets_of_runs(datasets)


def get_datasets_of_runs(datasets: List[Dict]) -> None:
    """
    Given a list of RunRegistry datasets, for each one:
    - Creates an OpenRuns object if it does not exist
    - If it exists, update the OpenRuns entry

    datasets is a list with dictionaries with lots of information, 
    including:
    - 'class'
    - 'name'
    - 'run_number'
    - 'lumisections'
    """
    today = timezone.now().strftime("%Y-%m-%d")

    for dataset in datasets:
        run_number = dataset["run_number"]
        logger.debug(f"Dataset {run_number}: {dataset['name']}")

        dataset_express = ""
        dataset_prompt = ""
        dataset_rereco = ""
        dataset_rereco_ul = ""
        state_express = ""
        state_prompt = ""
        state_rereco = ""
        state_rereco_ul = ""
        try:
            run_check = OpenRuns.objects.get(run_number=run_number)
        except OpenRuns.DoesNotExist:
            run_check = OpenRuns.objects.create(
                run_number=run_number,
                date_retrieved=today,
                dataset_express="",
                dataset_prompt="",
                dataset_rereco="",
                dataset_rereco_ul="",
                state_express="",
                state_prompt="",
                state_rereco="",
                state_rereco_ul="",
            )

        # Depending on the reconstruction type, update the
        # OpenRuns entry with the dataset name, if does not exist
        if "express" in dataset["name"].lower():
            dataset_express = dataset["name"]
            state_express = (dataset["dataset_attributes"]["tracker_state"]
                             if "tracker_state"
                             in dataset["dataset_attributes"] else "SIGNOFF")

            if not run_check.dataset_express:
                run_check.dataset_express = dataset_express
                run_check.state_express = state_express

        elif "prompt" in dataset["name"].lower():
            dataset_prompt = dataset["name"]
            state_prompt = (dataset["dataset_attributes"]["tracker_state"]
                            if "tracker_state" in dataset["dataset_attributes"]
                            else "SIGNOFF")
            if not run_check.dataset_prompt:
                run_check.dataset_prompt = dataset_prompt
                run_check.state_prompt = state_prompt

        elif "rereco" in dataset["name"].lower() and "UL" in dataset["name"]:
            dataset_rereco_ul = dataset["name"]
            state_rereco_ul = (dataset["dataset_attributes"]["tracker_state"]
                               if "tracker_state"
                               in dataset["dataset_attributes"] else "SIGNOFF")
            if not run_check.dataset_rereco_ul:
                run_check.dataset_rereco_ul = dataset_rereco_ul
                run_check.state_rereco_ul = state_rereco_ul

        elif "rereco" in dataset["name"].lower():
            dataset_rereco = dataset["name"]
            state_rereco = (dataset["dataset_attributes"]["tracker_state"]
                            if "tracker_state" in dataset["dataset_attributes"]
                            else "SIGNOFF")
            if not run_check.dataset_rereco:
                run_check.dataset_rereco = dataset_rereco
                run_check.state_rereco = state_rereco

        run_check.save()
