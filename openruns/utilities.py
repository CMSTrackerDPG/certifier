import runregistry
from django.utils import timezone
from wbmcrawlr import oms
from openruns.models import OpenRuns
from oms.utils import get_reco_from_dataset

def get_specific_open_runs(runs_list, user):
    runs = runregistry.get_runs(filter={
        'state':'OPEN',
        'run_number': {'or': runs_list},
    })

    get_datasets_of_runs(runs, user)

def get_open_runs(start, end, user):
    runs = runregistry.get_runs(filter={
        'state':'OPEN',
        'run_number': {'and': [{'>': start}, {'<': end}]},
    })

    get_datasets_of_runs(runs, user)

def get_datasets_of_runs(runs, user):
    for run in runs:
        datasets = runregistry.get_datasets(
            filter={
                'run_number': {
                    '=': run["run_number"]
                }
            }
        )

        today = timezone.now().strftime("%Y-%m-%d")

        run_check = OpenRuns.objects.filter(run_number=run["run_number"])
        if not run_check.exists():
            dataset_express=""
            dataset_prompt=""
            dataset_rereco=""

            for dataset in datasets:
                if "express" in dataset["name"].lower():
                    dataset_express=dataset["name"]
                if "prompt" in dataset["name"].lower():
                    dataset_prompt=dataset["name"]
                if "rereco" in dataset["name"].lower():
                    dataset_rereco=dataset["name"]

            if dataset_express!="":
                OpenRuns.objects.create(run_number=run["run_number"], dataset_express=dataset_express, user=user, date_retrieved=today)
                OpenRuns.objects.filter(run_number=run["run_number"]).update(dataset_prompt=dataset_prompt)
                OpenRuns.objects.filter(run_number=run["run_number"]).update(dataset_rereco=dataset_rereco)
        else:
            run_check.update(date_retrieved=today)
