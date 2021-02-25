import runregistry
from django.utils import timezone
from wbmcrawlr import oms
from openruns.models import OpenRuns
from oms.utils import get_reco_from_dataset

def get_specific_open_runs(runs_list, user):
    runs = runregistry.get_runs(filter={
        'run_number': {'or': runs_list},
    })

    get_datasets_of_runs(runs, user)

def get_open_runs(start, end, user):
    runs = runregistry.get_runs(filter={
        'run_number': {'and': [{'>': start}, {'<': end}]}
    })

    get_datasets_of_runs(runs, user)

def get_datasets_of_runs(runs, user):
    for run in runs:
        datasets = runregistry.get_datasets(
            filter={
                'run_number': {
                    '=': run["run_number"]
                },
                'global_state': {
                    '=': 'OPEN'
                },
            }
        )

        today = timezone.now().strftime("%Y-%m-%d")

        run_check = OpenRuns.objects.filter(run_number=run["run_number"])
        if not run_check.exists():
            dataset_express=""
            dataset_prompt=""
            dataset_rereco=""
            dataset_rereco_ul=""
            state_express=""
            state_prompt=""
            state_rereco=""
            state_rereco_ul=""
            for dataset in datasets:
                if "express" in dataset["name"].lower():
                    dataset_express=dataset["name"]
                    state_express=dataset["dataset_attributes"]["global_state"] if "global_state" in dataset["dataset_attributes"] else "SIGNOFF"
                elif "prompt" in dataset["name"].lower():
                    dataset_prompt=dataset["name"]
                    state_prompt=dataset["dataset_attributes"]["global_state"] if "global_state" in dataset["dataset_attributes"] else "SIGNOFF"
                elif "rereco" in dataset["name"].lower() and "UL" in dataset["name"]:
                    dataset_rereco_ul=dataset["name"]
                    state_rereco_ul=dataset["dataset_attributes"]["global_state"] if "global_state" in dataset["dataset_attributes"] else "SIGNOFF"
                elif "rereco" in dataset["name"].lower():
                    dataset_rereco=dataset["name"]
                    state_rereco=dataset["dataset_attributes"]["global_state"] if "global_state" in dataset["dataset_attributes"] else "SIGNOFF"

            if dataset_express!="" or dataset_prompt!="" or dataset_rereco!="" or dataset_rereco_ul!="":
                OpenRuns.objects.create(run_number=run["run_number"], dataset_express=dataset_express, user=user, state_express=state_express, date_retrieved=today)
                OpenRuns.objects.filter(run_number=run["run_number"]).update(dataset_prompt=dataset_prompt, state_prompt=state_prompt)
                OpenRuns.objects.filter(run_number=run["run_number"]).update(dataset_rereco=dataset_rereco, state_rereco=state_rereco)
                OpenRuns.objects.filter(run_number=run["run_number"]).update(dataset_rereco_ul=dataset_rereco_ul, state_rereco_ul=state_rereco_ul)
        else:
            run_check.update(date_retrieved=today)
