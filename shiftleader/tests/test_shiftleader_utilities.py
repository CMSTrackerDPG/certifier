from decimal import Decimal

import pytest
from mixer.backend.django import mixer
from shiftleader.utilities.utilities import *

from unittest.mock import MagicMock
from runregistry.client import RunRegistryClient
pytestmark = pytest.mark.django_db

class TestUtilities:
    def test_to_date(self):
        assert datetime.date(2010, 5, 17) == to_date(datetime.datetime(2010, 5, 17))
        assert datetime.date(2010, 5, 17) == to_date(datetime.date(2010, 5, 17))
        assert datetime.date(2010, 5, 17) == to_date("2010-05-17")

    def test_chunks(self):
        assert [range(10, 20), range(20, 29)] == list(chunks(range(10, 29), 10))

    def test_convert_run_registry_to_trackercertification(self):
        runregistry = RunRegistryClient()

        runregistry._get_query_id = MagicMock(return_value="o1662d3e8bb1")
        runregistry._get_json_response = MagicMock(
            return_value={"data": [[247073], [247076], [247077], [247078], [247079]]}
        )

        runregistry.connection_possible = MagicMock(return_value=True)

        query = (
            "select r.runnumber r.run_class r.dataset from runreg_global.runs r "
            "where r.run_class_name = 'Collisions15' "
            "and r.runnumber > 247070 and r.runnumber < 247081"
        )

        response = runregistry.execute_query(query)

        print(response)

