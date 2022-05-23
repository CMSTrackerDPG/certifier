import pytest

# import types
# from django.test import RequestFactory
# from mixer.backend.django import mixer
from oms.models import OmsFill, OmsRun
from oms.utils import oms_retrieve_fill, oms_retrieve_run

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
