import runregistry
from wbmcrawlr import oms
from openruns.models import OpenRuns
from oms.utils import get_reco_from_dataset

def get_open_runs(start, end, user):
    runs = runregistry.get_runs(filter={
        #'state':'OPEN',
        'run_number': {'and': [{'>': start}, {'<': end}]},
    })

    for run in runs:
        datasets = runregistry.get_datasets(
            filter={
                'run_number': {
                    '=': run["run_number"]
                }
            }
        )

        if not OpenRuns.objects.filter(run_number=run["run_number"]).exists():
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
                OpenRuns.objects.create(run_number=run["run_number"], dataset_express=dataset_express, user=user)
                OpenRuns.objects.filter(run_number=run["run_number"]).update(dataset_prompt=dataset_prompt)
                OpenRuns.objects.filter(run_number=run["run_number"]).update(dataset_rereco=dataset_rereco)

