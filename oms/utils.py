from django.db import IntegrityError, transaction
import runregistry
from omsapi.utilities import get_oms_run, get_oms_lumisection_count, get_oms_fill
from oms.models import OmsFill, OmsRun
from certifier.models import TrackerCertification


def get_reco_from_dataset(dataset):
    if "express" in dataset.lower():
        return "express"
    elif "prompt" in dataset.lower():
        return "prompt"
    elif "rereco" in  dataset.lower() and "UL" in dataset:
        return "rerecoul"
    elif "rereco" in  dataset.lower():
        return "rereco"

def retrieve_dataset_by_reco(run_number, reco):
    datasets = runregistry.get_datasets(
            filter={
                'run_number': {
                    '=': run_number
                }
            })

    for dataset in datasets:
        if reco in dataset["name"].lower():
            return dataset["name"]

        if reco == "rereco":
            if reco in dataset["name"].lower() and "UL" not in dataset["name"]:
                return dataset["name"]

        if reco == "rerecoul":
            if "rereco" in dataset["name"].lower() and "UL" in dataset["name"]:
                return dataset["name"]

    raise Exception("Could not find reconstruction:{} for run {}".format(reco, run_number))

def retrieve_dataset(run_number):
    datasets = runregistry.get_datasets(
            filter={
                'run_number': {
                    '=': run_number
                }
            })

    for dataset in datasets:
        if "online" not in dataset["name"]:
            if not TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number, runreconstruction__reconstruction=get_reco_from_dataset(dataset["name"])).exists():
                return dataset["name"]

    if len(datasets) == 0:
        raise Exception("No available datasets for run {}".format(run_number))
    else:
        raise Exception("Run {} has been fully certified".format(run_number))

def retrieve_fill(fill_number):
    fill_check = OmsFill.objects.filter(fill_number=fill_number) 

    if fill_check.exists():
        return OmsFill.objects.get(fill_number=fill_number)

    else:
        response = get_oms_fill(fill_number)
        if response == None:
            raise IndexError
        
        include_attribute_keys = ['fill_number', 'b_field', 'beta_star', 'bunches_beam1', 'bunches_beam2', 
        'bunches_colliding', 'bunches_target', 'crossing_angle', 'delivered_lumi', 'downtime', 'duration', 
        'efficiency_lumi', 'efficiency_time', 'energy', 'era', 'fill_type_party1', 'fill_type_party2', 
        'fill_type_runtime', 'init_lumi', 'injection_scheme', 'intensity_beam1', 'intensity_beam2', 'peak_lumi', 
        'peak_pileup', 'peak_specific_lumi', 'recorded_lumi', 'b_field_unit', 'peak_lumi_unit', 'beta_star_unit', 
        'init_lumi_unit', 'peak_specific_lumi_unit', 'intensity_beam2_unit', 'intensity_beam1_unit', 
        'delivered_lumi_unit', 'recorded_lumi_unit', 'crossing_angle_unit', 'energy_unit', 'first_run_number', 
        'last_run_number']

        include_meta_keys = ['init_lumi', 'peak_lumi', 'delivered_lumi', 'recorded_lumi', 'intensity_beam2', 
        'intensity_beam1', 'crossing_angle', 'peak_specific_lumi', 'beta_star']

        fill_kwargs = {key: value for key, value in response['attributes'] if key in include_attribute_keys}

        for meta_key in include_meta_keys:
            meta_key_unit = meta_key + "_unit"
            if response['meta']['row'][meta_key]['units']:
                fill_kwargs[meta_key_unit] = response['meta']['row'][meta_key]['units']

        try:
            with transaction.atomic():
                OmsFill.objects.create(**fill_kwargs)
        except IntegrityError:
            OmsFill.objects.filter(fill_number=fill_number).update(**fill_kwargs)

        return OmsFill.objects.get(fill_number=fill_number)

def retrieve_run(run_number):
    run_check = OmsRun.objects.filter(run_number=run_number) 

    if run_check.exists():
        return OmsRun.objects.get(run_number=run_number)

    else:
        response = get_oms_run(run_number)
        if response == None:
            raise IndexError

        fill_number = response.pop("fill_number")
        fill = retrieve_fill(fill_number=fill_number)

        include_attribute_keys = ["run_number", "run_type", "fill", "lumisections", "b_field", "clock_type", 
        "cmssw_version", "components", "delivered_lumi", "duration", "end_lumi", "energy", 
        "fill_type_party1", "fill_type_party2", "fill_type_runtime", "hlt_key", "hlt_physics_counter", 
        "hlt_physics_rate", "hlt_physics_size", "hlt_physics_throughput", "init_lumi", "initial_prescale_index", 
        "l1_hlt_mode", "l1_hlt_mode_stripped", "l1_key", "l1_key_stripped", "l1_menu", "l1_rate", 
        "l1_triggers_counter", "recorded_lumi", "sequence", "stable_beam", "tier0_transfer", "trigger_mode", 
        "b_field_unit", "init_lumi_unit", "delivered_lumi_unit", "recorded_lumi_unit", "end_lumi_unit", 
        "energy_unit"]

        include_meta_keys = ["init_lumi", "end_lumi", "delivered_lumi", "recorded_lumi"]

        run_kwargs = {key: value for key, value in response['attributes'] if key in include_attribute_keys}

        for meta_key in include_meta_keys:
            meta_key_unit = meta_key + "_unit"
            if response['meta']['row'][meta_key]['units']:
                run_kwargs[meta_key_unit] = response['meta']['row'][meta_key]['units']

        run_kwargs["lumisections"] = get_oms_lumisection_count(run_number)

        try:
            with transaction.atomic():
                OmsRun.objects.create(fill=fill, **run_kwargs)
        except IntegrityError:
            OmsRun.objects.filter(run_number=run_number).update(**run_kwargs)

        return OmsRun.objects.get(run_number=run_number)
