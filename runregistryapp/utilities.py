def transform_lowstat_to_boolean(list_of_run_dict):
    """
    Converts the low_stat properties of the list of run dictionaries into
    a boolean form

    True for low statistics
    False for no low statistics

    :param list_of_run_dict: list of runs (as dictionary)
    :return: list_of_run_dict
    """
    for run in list_of_run_dict:
        run["pixel_lowstat"] = run["pixel_lowstat"] == "LOW_STATS"
        run["sistrip_lowstat"] = run["sistrip_lowstat"] == "LOW_STATS"
        run["tracking_lowstat"] = run["tracking_lowstat"] == "LOW_STATS"
    return list_of_run_dict


def list_as_comma_separated_string(items):
    """
    Converts a list of items into a single comma separated string
    of single quoted items

    :param items: list of items
    :return: comma separated string of quoted items
    """
    return ", ".join(["'" + str(item) + "'" for item in items])


def list_to_dict(list_of_lists, keys):
    """
    Turns a list of lists into a list of dictionaries

    :param list_of_lists: list of lists
    :param keys: keys for the dictionary
    :return: list of dictionaries
    """
    return [dict(zip(keys, item)) for item in list_of_lists]


def build_list_where_clause(item_list, attribute):
    items = list_as_comma_separated_string(item_list)
    return "{} in ({})".format(attribute, items)


def build_range_where_clause(range_from, range_to, attribute):
    return "{} >= '{}' and {} <= '{}'".format(
        attribute, range_from, attribute, range_to
    )
