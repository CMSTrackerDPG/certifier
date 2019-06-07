import unittest
from unittest.mock import MagicMock

from runregistry.client import RunRegistryClient
from runregistry.utilities import *


class TestRunRegistryClient(unittest.TestCase):
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


class TestUtilities(unittest.TestCase):
    def test_transform_lowstat_to_boolean(self):
        run_dict = {
            "pixel_lowstat": "LOW_STATS",
            "sistrip_lowstat": "Bla",
            "tracking_lowstat": "LOW_STATS",
        }

        transform_lowstat_to_boolean([run_dict])

        self.assertTrue(run_dict["pixel_lowstat"])
        self.assertFalse(run_dict["sistrip_lowstat"])
        self.assertTrue(run_dict["tracking_lowstat"])

        run_dict = {
            "pixel_lowstat": 123,
            "sistrip_lowstat": "LOW_STATS",
            "tracking_lowstat": None,
        }

        transform_lowstat_to_boolean([run_dict])

        self.assertFalse(run_dict["pixel_lowstat"])
        self.assertTrue(run_dict["sistrip_lowstat"])
        self.assertFalse(run_dict["tracking_lowstat"])

    def test_list_as_comma_separated_string(self):
        run_list = ["123", 4234, "-1"]
        run_list_string = list_as_comma_separated_string(run_list)
        self.assertEqual("'123', '4234', '-1'", run_list_string)

    def test_list_to_dict(self):
        list_of_lists = [["a", "b", "c"], [None, 999, "f"], [-1, "h", "i"]]
        keys = ["x", "y", "z"]

        list_of_dicts = list_to_dict(list_of_lists, keys)

        expected_dict_list = [
            {"x": "a", "y": "b", "z": "c"},
            {"x": None, "y": 999, "z": "f"},
            {"x": -1, "y": "h", "z": "i"},
        ]

        self.assertEqual(expected_dict_list, list_of_dicts)

    def test_build_list_where_clause(self):
        run_list = ["123", 4234, "-1"]
        attribute = "123"
        list_where_clause = build_list_where_clause(run_list, attribute)
        self.assertEqual("123 in ('123', '4234', '-1')", list_where_clause)

    def test_build_range_where_clause(self):
        attribute = "123"
        range_from = "100"
        range_to = "200"
        range_where_clause = build_range_where_clause(range_from, range_to, attribute)
        self.assertEqual("123 >= '100' and 123 <= '200'", range_where_clause)
