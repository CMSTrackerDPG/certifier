import pytest

# import types
# from django.test import RequestFactory
from mixer.backend.django import mixer
from oms.models import OmsFill, OmsRun

pytestmark = pytest.mark.django_db


def test_oms_update_apv_mode_valid_run_number():
    run_number = 349422
    omsrun = mixer.blend(OmsRun, run_number=run_number)
    assert omsrun.apv_mode == "DECO"


def test_oms_update_apv_mode_invalid_run_number():
    run_number = 9999999
    with pytest.raises(ValueError):
        omsrun = mixer.blend(OmsRun, run_number=run_number)
