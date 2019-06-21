from decimal import Decimal

import pytest
from mixer.backend.django import mixer
from shiftleader.utilities.utilities import *

from unittest.mock import MagicMock
from runregistry.client import RunRegistryClient, TrackerRunRegistryClient
pytestmark = pytest.mark.django_db

class TestUtilities:
    def test_to_date(self):
        assert datetime.date(2010, 5, 17) == to_date(datetime.datetime(2010, 5, 17))
        assert datetime.date(2010, 5, 17) == to_date(datetime.date(2010, 5, 17))
        assert datetime.date(2010, 5, 17) == to_date("2010-05-17")

    def test_chunks(self):
        assert [range(10, 20), range(20, 29)] == list(chunks(range(10, 29), 10))

    def test_convert_run_registry_to_trackercertification(self):
        input=[{'run_number': 319449, 'run_class': '', 'dataset': '/Express/Collisions2018/DQM', 'state': 'COMPLETED', 'shifter': 'Franco Ligabue', 'pixel': 'GOOD', 'sistrip': 'GOOD', 'tracking': 'GOOD', 'pixel_lowstat': False, 'sistrip_lowstat': False, 'tracking_lowstat': False}, {'run_number': 319449, 'run_class': 'Collisions18', 'dataset': '/ReReco/Run2018C_17Sept2018/DQM', 'state': 'COMPLETED', 'shifter': 'Subir Sarkar', 'pixel': 'GOOD', 'sistrip': 'GOOD', 'tracking': 'GOOD', 'pixel_lowstat': False, 'sistrip_lowstat': False, 'tracking_lowstat': False}, {'run_number': 327589, 'run_class': '', 'dataset': '/Express/HICosmics2018/DQM', 'state': 'COMPLETED', 'shifter': 'Roberval Walsh Bastos Rangel', 'pixel': 'EXCLUDED', 'sistrip': 'GOOD', 'tracking': 'GOOD', 'pixel_lowstat': False, 'sistrip_lowstat': False, 'tracking_lowstat': False}, {'run_number': 327589, 'run_class': 'Cosmics18', 'dataset': '/PromptReco/HICosmics18A/DQM', 'state': 'COMPLETED', 'shifter': 'Suchandra Dutta', 'pixel': 'EXCLUDED', 'sistrip': 'GOOD', 'tracking': 'GOOD', 'pixel_lowstat': False, 'sistrip_lowstat': False, 'tracking_lowstat': False}]

        ret = convert_run_registry_to_trackercertification(input)

        assert [{'state': 'COMPLETED', 'shifter': 'Franco Ligabue', 'pixel': 'Good', 'sistrip': 'GOOD', 'tracking': 'Good', 'pixel_lowstat': False, 'tracking_lowstat': False, 'dataset': '/Express/Collisions2018/DQM', 'runreconstruction__run__run_number': 319449, 'runreconstruction__run__run_type': 'collisions', 'runreconstruction__reconstruction': 'express', 'strip': 'Good', 'strip_lowstat': False}, {'state': 'COMPLETED', 'shifter': 'Subir Sarkar', 'pixel': 'Good', 'sistrip': 'GOOD', 'tracking': 'Good', 'pixel_lowstat': False, 'tracking_lowstat': False, 'dataset': '/ReReco/Run2018C_17Sept2018/DQM', 'runreconstruction__run__run_number': 319449, 'runreconstruction__run__run_type': 'collisions', 'runreconstruction__reconstruction': 'rereco', 'strip': 'Good', 'strip_lowstat': False}, {'state': 'COMPLETED', 'shifter': 'Roberval Walsh Bastos Rangel', 'pixel': 'Excluded', 'sistrip': 'GOOD', 'tracking': 'Good', 'pixel_lowstat': False, 'tracking_lowstat': False, 'dataset': '/Express/HICosmics2018/DQM', 'runreconstruction__run__run_number': 327589, 'runreconstruction__run__run_type': 'cosmics', 'runreconstruction__reconstruction': 'express', 'strip': 'Good', 'strip_lowstat': False}, {'state': 'COMPLETED', 'shifter': 'Suchandra Dutta', 'pixel': 'Excluded', 'sistrip': 'GOOD', 'tracking': 'Good', 'pixel_lowstat': False, 'tracking_lowstat': False, 'dataset': '/PromptReco/HICosmics18A/DQM', 'runreconstruction__run__run_number': 327589, 'runreconstruction__run__run_type': 'cosmics', 'runreconstruction__reconstruction': 'prompt', 'strip': 'Good', 'strip_lowstat': False}] == ret


