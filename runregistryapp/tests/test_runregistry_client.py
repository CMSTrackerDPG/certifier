import unittest
import pytest
from unittest.mock import MagicMock

from runregistryapp.client import RunRegistryClient, TrackerRunRegistryClient
from runregistryapp.utilities import *


class TestRunRegistryClient(unittest.TestCase):
    def test_get_json_response(self):
        runregistry = RunRegistryClient("http://vocms00170:4367")
        assert {} == runregistry._get_json_response(resource=None, media_type=None)

        runregistry.url = runregistry.DEFAULT_URL
        runregistry.retry_connection()
        query = (
            "select r.runnumber from runreg_global.runs r "
            "where r.run_class_name = 'Collisions15' "
            "and r.runnumber > 247070 and r.runnumber < 247081"
        )

        expected_response = {"data": [[247073], [247076], [247077], [247078], [247079]]}
        response = runregistry.execute_query(query)
        self.assertEqual(expected_response, response)
        response = runregistry.execute_query(query, "text/json")
        self.assertEqual("Unsupported media types", response)

    def test_get_query_id(self):
        runregistry = RunRegistryClient()
        query = (
            "select r.runclass r.run_number.rom runreg_global.runs "
            "where r.run_class_name = 'Collisions15' "
            "and r.runnumber > 247070 and r.runnumber < 247081"
        )

        with pytest.raises(ValueError):
            response = runregistry.execute_query(query)
            assert "ValueError" in response


    def test_connection(self):
        runregistry = RunRegistryClient("http://vocms00170:4367")
        assert False == runregistry._test_connection()
        assert False == runregistry.connection_possible()

        runregistry.url = runregistry.DEFAULT_URL
        assert True == runregistry._test_connection()
        assert True == runregistry.connection_possible()

    def test_execute_query(self):
        runregistry = RunRegistryClient()

        runregistry._get_query_id = MagicMock(return_value="o1662d3e8bb1")
        runregistry._get_json_response = MagicMock(
            return_value={"data": [[247073], [247076], [247077], [247078], [247079]]}
        )

        runregistry.connection_possible = MagicMock(return_value=True)

        query = (
            "select r.runnumber from runreg_global.runs r "
            "where r.run_class_name = 'Collisions15' "
            "and r.runnumber > 247070 and r.runnumber < 247081"
        )

        response = runregistry.execute_query(query)
        expected_response = {"data": [[247073], [247076], [247077], [247078], [247079]]}

        self.assertEqual(expected_response, response)
        runregistry._get_query_id.assert_called_with(query)
        runregistry._get_json_response.assert_called_with(
            "/query/o1662d3e8bb1/data", None
        )

        runregistry = RunRegistryClient()
        runregistry.url="http://vocms00170:4367"
        runregistry.retry_connection()

        response = runregistry.execute_query(query)
        assert {} == response

        runregistry.url=runregistry.DEFAULT_URL

    def test_get_table_description(self):
        runregistry = RunRegistryClient()
        response = runregistry.get_table_description()
        assert {'workspace': 'TRACKER', 'application': 'USER', 'description': 'Dataset lumisections including exceptions', 'Source': '/org/cern/cms/dqm/runregistry/workspace.xml'} == response["metadata"]

    def test_get_queries(self):
        runregistry = RunRegistryClient()
        response = runregistry.get_queries()
        assert {} != response

    def test_get_query_description(self):
        runregistry = RunRegistryClient()
        response = runregistry.get_queries()
        query_keys=list(response.keys())
        response = runregistry.get_query_description(query_keys[0])
        assert {} != response

    def test_get_info(self):
        runregistry = RunRegistryClient()
        response = runregistry.get_info()
        assert {} != response

class TestTrackerRunRegistryClient(unittest.TestCase):
    def test_get_dataset_lumis_runs(self):
        runregistry=TrackerRunRegistryClient()
        where_clause = build_list_where_clause(["321123"], "r.rdr_run_number") 
        response = runregistry._get_dataset_lumis_runs(where_clause)
        assert response

    def test_get_dataset_runs_with_active_lumis(self):
        runregistry=TrackerRunRegistryClient()
        where_clause = build_list_where_clause(["321123"], "r.run_number") 
        response = runregistry._get_dataset_runs_with_active_lumis(where_clause)
        assert response

    def test_get_runs_by_list(self):
        runregistry=TrackerRunRegistryClient()
        run_number=321123
        response = runregistry.get_runs_by_list(None)
        assert [] == response
        response = runregistry.get_runs_by_list([run_number])
        assert response[0]["run_number"] == run_number

    def test_get_runs_by_range(self):
        runregistry=TrackerRunRegistryClient()
        run_min=321123
        run_max=321126
        response = runregistry.get_runs_by_range(run_min, run_max)
        assert run_min == response[0]["run_number"] and run_max == response[len(response)-1]["run_number"]

    def test_get_lumi_sections_by_list(self):
        runregistry=TrackerRunRegistryClient()
        run_number=321123
        response = runregistry.get_lumi_sections_by_list([run_number])
        assert response[0]["run_number"] == run_number

    def test_get_lumi_sections_by_range(self):
        runregistry=TrackerRunRegistryClient()
        run_min=321123
        run_max=321126
        response = runregistry.get_lumi_sections_by_range(run_min, run_max)
        assert run_min == response[0]["run_number"] and run_max == response[len(response)-1]["run_number"]

    def test_get_active_lumi_runs_by_list(self):
        runregistry=TrackerRunRegistryClient()
        run_number=321123
        response = runregistry.get_active_lumi_runs_by_list([run_number])
        assert response[0]["run_number"] == run_number

    def test_get_active_lumi_runs_by_range(self):
        runregistry=TrackerRunRegistryClient()
        run_min=321123
        run_max=321126
        response = runregistry.get_active_lumi_runs_by_range(run_min, run_max)
        assert run_min == response[0]["run_number"] and run_max == response[len(response)-1]["run_number"]

    def test_get_run_numbers_by_fill_number(self):
        runregistry=TrackerRunRegistryClient()
        response = runregistry.get_run_numbers_by_fill_number([7048, 7049])
        assert  [{'fill_number': 7048, 'run_number': [321171, 321174, 321175, 321177, 321178, 321179, 321181]}, {'fill_number': 7049, 'run_number': [321182, 321185, 321189]}] == response
