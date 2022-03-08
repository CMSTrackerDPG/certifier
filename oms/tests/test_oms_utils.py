import pytest
# import types
# from django.test import RequestFactory
# from mixer.backend.django import mixer

from oms.utils import retrieve_fill, retrieve_run

pytestmark = pytest.mark.django_db


def test_retrieve_fill():
    fill_number = 7044
    retrieve_fill(fill_number)
    retrieve_fill(fill_number)

    # Will use omsapi to get fill
    assert OmsFill.objects.get(fill_number=fill_number)


def test_retrieve_run():
    run_number = 321123
    retrieve_run(run_number)
    retrieve_run(run_number)

    assert OmsRun.objects.get(run_number=run_number)
