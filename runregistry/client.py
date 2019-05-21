""""
RunRegistry Client
"""
from itertools import groupby
from json import JSONDecodeError
from operator import itemgetter

import requests

from runregistry.utilities import (
    transform_lowstat_to_boolean,
    list_to_dict,
    build_range_where_clause,
    build_list_where_clause,
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RunRegistryClient(metaclass=Singleton):
    """
    Implements a simple client that accesses the RunRegistry through the resthub API

    See:
    https://github.com/valdasraps/resthub
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/DqmRrApi
    """

    DEFAULT_URL = "http://vocms00170:2113"
    ALTERNATIVE_URL = "http://cmsrunregistryapi.cern.ch:2113"

    DEFAULT_NAMESPACE = "runreg_tracker"
    DEFAULT_TABLE = "dataset_lumis"

    def __init__(self, url=DEFAULT_URL):
        self.url = url
        self._connection_successful = None  # Lazy

    def _test_connection(self):
        try:
            requests.get(self.url)
            return True
        except requests.ConnectionError:
            return False

    def retry_connection(self):
        """
        Retry to connect to Run Registry.
        Updates return value of the connection_possible method.
        """
        self._connection_successful = self._test_connection()

    def connection_possible(self):
        """
        Check if the connection to the Run Registry is possible.

        Example:
        >>> client = RunRegistryClient()
        >>> client.connection_possible()
        True

        :return: True when connection to Run Registry was successful
        """
        if self._connection_successful is None:
            self.retry_connection()
        return self._connection_successful

    def _get_json_response(self, resource, media_type=None):
        if not self.connection_possible():
            return {}

        if media_type:
            headers = {"Accept": media_type}
            response = requests.get(self.url + resource, headers=headers)
            return response.content.decode("utf-8")

        try:
            response = requests.get(self.url + resource)
            return response.json()
        except JSONDecodeError:
            return {}

    def _get_query_id(self, query):
        """
        Converts a SQL query string into a query id (qid), that will be used to access
        the RunRegistry.

        POST: /query

        :param query: SQL query string
        :return: query id
        """
        response = requests.post(self.url + "/query?", data=query)
        if response.status_code == 400:
            raise ValueError(response.text)
        return response.text

    def execute_query(self, query, media_type=None):
        """
        Executes an arbitrary SQL query

        GET: /query/{query_id}

        Limitations:
         - tables referred by namespace.table
         - all tables used must have the unique alias in a query
         - only tables that share the same connection can be used in a query
         - named parameters are supported, i.e. :name
         - by default named parameter is considered of string type
         - named parameter type can be changed with prefix:
           - s__{parameter name} string type, i.e. s__name, s__country
           - n__{parameter name} number type, i.e. n__id, n__voltage
           - d__{parameter name} date type, i.e. d__from, d__to
         - supported functions can be found under /info

        Example:
        >>> client = RunRegistryClient()
        >>> query = "select r.runnumber from runreg_global.runs r " \
                    "where r.run_class_name = 'Collisions15'" \
                    "and r.runnumber > 247070 and r.runnumber < 247081"
        >>> client.execute_query(query)
        {'data': [[247073], [247076], [247077], [247078], [247079]]}

        :param media_type: Desired media type, e.g. application/xml, text/json
        :param query: SQL query string
        :return: JSON dictionary
        """
        if not self.connection_possible():
            return {}
        query_id = self._get_query_id(query)
        resource = "/query/" + query_id + "/data"
        return self._get_json_response(resource, media_type)

    def get_table_description(self, namespace=DEFAULT_NAMESPACE, table=DEFAULT_TABLE):
        """
        Table description in JSON

        Example:
        >>> client = RunRegistryClient()
        >>> client.get_table_description("runreg_tracker", "dataset_lumis")["metadata"]["description"]
        'Dataset lumisections including exceptions'

        :param namespace: runreg_{workspace}, e.g. runreg_tracker
        :param table: runs, run_lumis, datasets, dataset_lumis
        :return: json containing the table description
        """
        resource = "/table/{}/{}".format(namespace, table)
        return self._get_json_response(resource)

    def get_queries(self):
        """
        GET /queries/

        :return: list of queries
        """
        return self._get_json_response("/queries")

    def get_query_description(self, query_id):
        """
        GET /query/{query_id}

        :return: json dictionary with query description
        """
        return self._get_json_response("/query/{}".format(query_id))

    def get_info(self):
        """
        GET /info

        Contains a list of supported functions and the version numbers.

        Example:
        >>> client = RunRegistryClient()
        >>> client.get_info()["version"]["resthub"]
        '0.6.18'

        :return json with general information about the service
        """
        return self._get_json_response("/info")


class TrackerRunRegistryClient(RunRegistryClient):
    """
    Client to access the Tracker Workspace of the Run Registry

    https://cmswbmoffshift.web.cern.ch/cmswbmoffshift/runregistry_offline/index.jsf
    """

    def __get_dataset_runs(self, where_clause):
        query = (
            "select r.run_number, r.run_class_name, r.rda_name, r.rda_state, "
            "r.rda_last_shifter, r.rda_cmp_pixel, r.rda_cmp_strip, "
            "r.rda_cmp_tracking, r.rda_cmp_pixel_cause, r.rda_cmp_strip_cause, "
            "r.rda_cmp_tracking_cause "
            "from runreg_tracker.datasets r "
            "where {} "
            "and r.rda_name != '/Global/Online/ALL'".format(where_clause)
        )

        run_list = self.execute_query(query).get("data", [])

        keys = [
            "run_number",
            "run_class",
            "dataset",
            "state",
            "shifter",
            "pixel",
            "sistrip",
            "tracking",
            "pixel_lowstat",
            "sistrip_lowstat",
            "tracking_lowstat",
        ]

        run_dicts = list_to_dict(run_list, keys)
        transform_lowstat_to_boolean(run_dicts)

        return run_dicts

    def __get_dataset_lumis_runs(self, where_clause):
        query = (
            "select r.rdr_run_number, r.lhcfill, r.rdr_rda_name, r.rdr_section_from, "
            "r.rdr_section_to, r.rdr_section_count, "
            "r.cms_active, r.beam1_stable, r.beam2_stable, r.beam1_present, "
            "r.beam2_present, r.tibtid_ready, r.tob_ready, r.tecp_ready, "
            "r.tecm_ready, r.bpix_ready, r.fpix_ready "
            "from runreg_tracker.dataset_lumis r "
            "where r.rdr_rda_name != '/Global/Online/ALL' "
            "and {} "
            "order by r.rdr_run_number, r.rdr_rda_name, r.rdr_range".format(
                where_clause
            )
        )

        run_list = self.execute_query(query).get("data", [])

        keys = [
            "run_number",
            "lhcfill",
            "dataset",
            "section_from",
            "section_to",
            "section_count",
            "cms_active",
            "beam1_stable",
            "beam2_stable",
            "beam1_present",
            "beam2_present",
            "tibtid",
            "tob",
            "tecp",
            "tecm",
            "bpix",
            "fpix",
        ]

        return list_to_dict(run_list, keys)

    def __get_dataset_runs_with_active_lumis(self, where_clause):
        query = (
            "select r.run_number, r.run_class_name, r.rda_name, "
            "sum(l.rdr_section_count) as lumi_sections, "
            "r.rda_state, r.rda_last_shifter, r.rda_cmp_pixel, r.rda_cmp_strip, "
            "r.rda_cmp_tracking, r.rda_cmp_pixel_cause, r.rda_cmp_strip_cause, "
            "r.rda_cmp_tracking_cause "
            "from runreg_tracker.dataset_lumis l, runreg_tracker.datasets r "
            "where l.rdr_run_number = r.run_number "
            "and l.rdr_rda_name = r.rda_name "
            "and l.rdr_rda_name != '/Global/Online/ALL' "
            "and l.cms_active = 1 "
            "and (l.beam1_stable = 1 "
            "and l.beam2_stable = 1 "
            "or l.rdr_rda_name LIKE '%Cosmics%') "
            "and l.TIBTID_READY = 1 "
            "and l.TOB_READY = 1 "
            "and l.TECP_READY = 1 "
            "and l.TECM_READY = 1 "
            "and l.BPIX_READY = 1 "
            "and l.FPIX_READY = 1 "
            "and {} "
            "group by r.run_number, r.rda_name, r.run_class_name, "
            "r.rda_state, r.rda_last_shifter, r.rda_cmp_pixel, r.rda_cmp_strip, "
            "r.rda_cmp_tracking, r.rda_cmp_pixel_cause, r.rda_cmp_strip_cause, "
            "r.rda_cmp_tracking_cause ".format(where_clause)
        )

        run_list = self.execute_query(query).get("data", [])

        keys = [
            "run_number",
            "run_class",
            "dataset",
            "lumi_sections",
            "state",
            "shifter",
            "pixel",
            "sistrip",
            "tracking",
            "pixel_lowstat",
            "sistrip_lowstat",
            "tracking_lowstat",
        ]

        run_dict = list_to_dict(run_list, keys)
        transform_lowstat_to_boolean(run_dict)

        return run_dict

    def get_runs_by_list(self, list_of_run_numbers):
        """
        Get list of run dictionaries from the Tracker workspace in the Run Registry

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> runs = client.get_runs_by_list(["323423"])
        >>> runs[0]["state"]
        'COMPLETED'

        :param list_of_run_numbers: list of run numbers
        :return: dictionary containing the queryset
        """
        if not list_of_run_numbers:
            return []

        where_clause = build_list_where_clause(list_of_run_numbers, "r.run_number")
        return self.__get_dataset_runs(where_clause)

    def get_runs_by_range(self, min_run_number, max_run_number):
        """
        Get list of run dictionaries from the Tracker workspace in the Run Registry

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> runs = client.get_runs_by_range("323471", "323475")
        >>> runs[0]["run_class"]
        'Collisions18'

        :param min_run_number: first run number
        :param max_run_number: last run number
        :return: dictionary containing the queryset
        """
        where_clause = build_range_where_clause(
            min_run_number, max_run_number, "r.run_number"
        )
        return self.__get_dataset_runs(where_clause)

    def get_lumi_sections_by_list(self, list_of_run_numbers):
        """
        Get list of lumisections for the given run number list

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> lumis = client.get_lumi_sections_by_list(["323471"])
        >>> lumis[0]["lhcfill"]
        7217

        :param list_of_run_numbers:
        :return:
        """
        where_clause = build_list_where_clause(list_of_run_numbers, "r.rdr_run_number")
        return self.__get_dataset_lumis_runs(where_clause)

    def get_lumi_sections_by_range(self, min_run_number, max_run_number):
        """
        Get list of lumisections for the given run number range

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> lumis = client.get_lumi_sections_by_range("323472", "323485")
        >>> lumis[0]["section_count"]
        94

        :param min_run_number: first run number
        :param max_run_number: last run number
        :return: dictionary containing the queryset
        """
        where_clause = build_range_where_clause(
            min_run_number, max_run_number, "r.rdr_run_number"
        )
        return self.__get_dataset_lumis_runs(where_clause)

    def get_active_lumi_runs_by_list(self, list_of_run_numbers):
        """
        Get list of runs with certification status and active lumi sections

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> runs = client.get_active_lumi_runs_by_list(["321777"])
        >>> runs[0]["lumi_sections"]
        279
        """
        where_clause = build_list_where_clause(list_of_run_numbers, "r.run_number")
        return self.__get_dataset_runs_with_active_lumis(where_clause)

    def get_active_lumi_runs_by_range(self, min_run_number, max_run_number):
        """
        Get list of runs with certification status and active lumi sections

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> runs = client.get_active_lumi_runs_by_range("323472", "323485")
        >>> runs[0]["pixel"]
        'GOOD'
        """
        where_clause = build_range_where_clause(
            min_run_number, max_run_number, "r.run_number"
        )
        return self.__get_dataset_runs_with_active_lumis(where_clause)

    def get_fill_number_by_run_number(self, list_of_run_numbers):
        """
        Retrieve a list of fill numbers by the given run numbers

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> client.get_fill_number_by_run_number([321177, 321178, 321218])
        [{'run_number': 321177, 'fill_number': 7048}, {'run_number': 321178, 'fill_number': 7048}, {'run_number': 321218, 'fill_number': 7052}]

        :param list_of_run_numbers:
        :return: list of dictionaries containing run number and corresponding fill number
        """
        where_clause = build_list_where_clause(list_of_run_numbers, "r.runnumber")
        query = (
            "select r.runnumber, r.lhcfill "
            "from runreg_tracker.runs r "
            "where {} "
            "order by r.runnumber".format(where_clause)
        )
        items = self.execute_query(query).get("data", [])
        keys = ["run_number", "fill_number"]
        return list_to_dict(items, keys)

    def get_unique_fill_numbers_by_run_number(self, list_of_run_numbers):
        """
        Retrieve a list of unique fill numbers by the given run numbers

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> client.get_unique_fill_numbers_by_run_number([321177, 321178, 321218, 323500])
        [7048, 7052]

        :param list_of_run_numbers:
        :return: list of dictionaries containing run number and corresponding fill number
        """

        where_clause = build_list_where_clause(list_of_run_numbers, "r.runnumber")
        query = (
            "select r.lhcfill "
            "from runreg_tracker.runs r "
            "where {} "
            "order by r.runnumber".format(where_clause)
        )
        runs = self.execute_query(query).get("data", [])
        return sorted({run[0] for run in runs if run[0] is not None})

    def get_run_numbers_by_fill_number(self, list_of_fill_numbers):
        """
        Retrieve a list of run numbers by the given fill numbers

        Example:
        >>> client = TrackerRunRegistryClient()
        >>> client.get_run_numbers_by_fill_number([7048, 7049])
        [{'fill_number': 7048, 'run_number': [321171, 321174, 321175, 321177, 321178, 321179, 321181]}, {'fill_number': 7049, 'run_number': [321182, 321185, 321189]}]

        :param list_of_fill_numbers:
        :return: list of dictionaries containing fill number and corresponding
        list of run numbers
        """
        where_clause = build_list_where_clause(list_of_fill_numbers, "r.lhcfill")
        query = (
            "select r.lhcfill, r.runnumber "
            "from runreg_tracker.runs r "
            "where {} "
            "order by r.runnumber".format(where_clause)
        )
        response = self.execute_query(query).get("data", [])
        groups = groupby(response, itemgetter(0))
        items = [(key, [item[1] for item in value]) for key, value in groups]
        keys = ["fill_number", "run_number"]
        return list_to_dict(items, keys)

    def get_grouped_fill_numbers_by_run_number(self, list_of_run_numbers):
        """
        Example:
        >>> client = TrackerRunRegistryClient()
        >>> client.get_grouped_fill_numbers_by_run_number([321171, 321179, 321181, 321182, 321185])
        [{'fill_number': 7048, 'run_number': [321171, 321179, 321181]}, {'fill_number': 7049, 'run_number': [321182, 321185]}]
        """
        where_clause = build_list_where_clause(list_of_run_numbers, "r.runnumber")
        query = (
            "select r.lhcfill, r.runnumber "
            "from runreg_tracker.runs r "
            "where {} "
            "order by r.runnumber".format(where_clause)
        )
        response = self.execute_query(query).get("data", [])
        groups = groupby(response, itemgetter(0))
        items = [(key, [item[1] for item in value]) for key, value in groups]
        keys = ["fill_number", "run_number"]
        return list_to_dict(items, keys)
