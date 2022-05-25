import pytest

# import types
# from django.test import RequestFactory
# from mixer.backend.django import mixer
from oms.models import OmsFill, OmsRun
from oms.utils import oms_retrieve_fill, oms_retrieve_run, get_reco_from_dataset

pytestmark = pytest.mark.django_db


def test_oms_retrieve_fill():
    fill_number = 7044
    oms_retrieve_fill(fill_number)
    oms_retrieve_fill(fill_number)

    # Will use omsapi to get fill
    assert OmsFill.objects.get(fill_number=fill_number)


def test_oms_retrieve_run():
    run_number = 321123
    oms_retrieve_run(run_number)
    oms_retrieve_run(run_number)

    assert OmsRun.objects.get(run_number=run_number)


def test_reco_from_dataset():
    test_cases = [
        ("express", "/StreamExpressCosmics/Commissioning2018-Express-v1/DQMIO"),
        ("prompt", "/Cosmics/Commissioning2018-PromptReco-v1/DQMIO"),
        ("rereco", "/ReReco/Run2018A_17Sept2018/DQM"),
        ("rerecoul", "/ReReco/Run2017B_UL2019/DQM"),
    ]
    for case in test_cases:
        assert get_reco_from_dataset(case[1]) == case[0]
