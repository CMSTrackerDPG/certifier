from django.utils import timezone
import datetime

def to_date(date, formatstring="%Y-%m-%d"):
    if isinstance(date, datetime.datetime):
        return date.date()
    if isinstance(date, datetime.date):
        return date
    return datetime.datetime.strptime(date, formatstring).date()

def to_weekdayname(date, formatstring="%Y-%m-%d"):
    return to_date(date, formatstring).strftime("%A")

def get_this_week_filter_parameter():
    start_of_week = timezone.now() - timezone.timedelta(timezone.now().weekday())
    end_of_week = start_of_week + timezone.timedelta(6)

    date_gte = (
        str(start_of_week.year)
        + "-"
        + str(start_of_week.month)
        + "-"
        + str(start_of_week.day)
    )
    date_lte = (
        str(end_of_week.year)
        + "-"
        + str(end_of_week.month)
        + "-"
        + str(end_of_week.day)
    )

    get_parameters = "?date__gte=" + str(date_gte)
    get_parameters += "&date__lte=" + str(date_lte)

    return get_parameters

def get_certification_status(detector_type):
    if "GOOD" in detector_type.keys():
        return "Good"
    if "BAD" in detector_type.keys():
        return "Bad"
    if "EXCLUDED" in detector_type.keys():
        return "Excluded"

def convert_run_registry_to_trackercertification(list_of_dictionaries):
    """
    Converts the list of JSON dictionaries into a TrackerCertification compatible format, i.e.:

    :param list_of_dictionaries:
    :return:
    """
    for entry in list_of_dictionaries:
        run_class = entry.pop("class").lower()
        entry["dataset"] = entry.pop("name")
        dataset = entry["dataset"].lower()
        entry["runreconstruction__run__run_number"] = entry.pop("run_number")

        if "collision" in run_class:
            entry["runreconstruction__run__run_type"] = "collisions"
        elif "cosmic" in run_class:
            entry["runreconstruction__run__run_type"] = "cosmics"
        elif "collision" in dataset:  # When run_class is e.g. Commissioning18
            entry["runreconstruction__run__run_type"] = "collisions"
        elif "cosmic" in dataset:
            entry["runreconstruction__run__run_type"] = "cosmics"

        if "express" in dataset:
            entry["runreconstruction__reconstruction"] = "express"
        elif "prompt" in dataset:
            entry["runreconstruction__reconstruction"] = "prompt"
        elif "rereco" in dataset and "UL" in entry["dataset"]:
            entry["runreconstruction__reconstruction"] = "rerecoul"
        elif "rereco" in dataset:
            entry["runreconstruction__reconstruction"] = "rereco"

        entry["pixel"] = get_certification_status(entry["lumisections"]["tracker-pixel"]) if "tracker-pixel" in entry["lumisections"]  else None
        entry["strip"] = get_certification_status(entry["lumisections"]["tracker-strip"]) if "tracker-strip" in entry["lumisections"]  else None
        entry["tracking"] = get_certification_status(entry["lumisections"]["tracker-track"]) if "tracker-track" in entry["lumisections"]  else None


    return list_of_dictionaries


def chunks(elements_list, n):
    """
    Split a list into sublists of fixed length n

    Credit: https://stackoverflow.com/a/312464/9907540

    :param elements_list: list of elements that needs to be split
    :param n: chunk size of new lists
    """
    for index in range(0, len(elements_list), n):
        yield elements_list[index : index + n]
