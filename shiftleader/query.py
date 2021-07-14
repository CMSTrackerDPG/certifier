import collections

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.functions import Coalesce
from django.db.models import (
    Q,
    Count,
    Sum,
    FloatField,
    When,
    Case,
    Value,
    CharField,
    Min,
    Max,
)
from django.db.models.functions import ExtractWeekDay
from delete.query import SoftDeletionQuerySet
from shiftleader.utilities.utilities import convert_run_registry_to_trackercertification

import runregistry
from operator import itemgetter
from itertools import groupby

class TrackerCertificationQuerySet(SoftDeletionQuerySet):
    def annotate_status(self):
        return self.annotate(
            status=Case(
                When(
                    (Q(runreconstruction__run__run_type="cosmics") | Q(pixel="good") | Q(pixel_lowstat=True))
                    & (Q(strip="good") | Q(strip_lowstat=True))
                    & (Q(tracking="good") | Q(tracking_lowstat=True)),
                    then=Value("good"),
                ),
                default=Value("bad"),
                output_field=CharField(),
            )
        )

    def filter_flag_changed(self, until=None):
        """
        Filters the queryset to all runs where the flag has changed
        """
        from certifier.models import TrackerCertification

        # Group by unique run_number, status pairs
        # if a run_number appears more than once, it means that the flag changed

        runs = TrackerCertification.objects.all()
        if until:
            runs = runs.filter(date__lte=until)

        run_number_list = [
            run["runreconstruction__run__run_number"]
            for run in runs.annotate_status()
                .order_by("runreconstruction__run__run_number")
                .values("runreconstruction__run__run_number", "status")
                .annotate(times_certified=Count("runreconstruction__run__run_number"))
        ]

        changed_flag_runs = [
            run
            for run, count in collections.Counter(run_number_list).items()
            if count > 1
        ]

        return self.filter(runreconstruction__run__run_number__in=changed_flag_runs)

    def good(self):
        good_criteria = "good"

        return (
            self.filter(Q(strip=good_criteria) | Q(strip_lowstat=True))
                .filter(Q(tracking=good_criteria) | Q(tracking_lowstat=True))
                .filter(Q(runreconstruction__run__run_type="cosmics") | Q(pixel=good_criteria) | Q(pixel_lowstat=True))
                )

    def bad(self):
        bad_criteria = ["bad", "excluded"]

        return self.filter(
            (Q(strip__in=bad_criteria) & Q(strip_lowstat=False) )
            | (Q(tracking__in=bad_criteria) & Q(tracking_lowstat=False))
            | (Q(pixel__in=bad_criteria) & Q(pixel_lowstat=False) & Q(runreconstruction__run__run_type="collisions"))
        )

    def summary(self):
        """
        Create basic summary with int_luminosity and number_of_ls per type
        """
        summary_dict = (
            self.order_by("runreconstruction__run__run_type", "runreconstruction__reconstruction")
                .values("runreconstruction__run__run_type", "runreconstruction__reconstruction")
                .annotate(
                runs_certified=Count("pk"),
                int_luminosity=Sum("runreconstruction__run__recorded_lumi", output_field=FloatField()),
                number_of_ls=Sum("runreconstruction__run__lumisections"),
            )
        )

        """
        Add List of run_numbers per type to the summary
        """
        for d in summary_dict:
            runs_per_type = self.filter(
                runreconstruction__run__run_type=d.get("runreconstruction__run__run_type"), runreconstruction__reconstruction=d.get("runreconstruction__reconstruction")
            ).order_by("runreconstruction__run__run_number")

            good_run_numbers = [r.run_number for r in runs_per_type.good()]

            bad_run_numbers = [r.run_number for r in runs_per_type.bad()]

            d.update(
                {"run_numbers": {"good": good_run_numbers, "bad": bad_run_numbers}}
            )

        return summary_dict

    def summary_per_day(self):
        summary_dict = (
            self.order_by("date", "runreconstruction__run__run_type", "runreconstruction__reconstruction")
                .values("date", "runreconstruction__run__run_type", "runreconstruction__reconstruction")
                .annotate(
                runs_certified=Count("pk"),
                int_luminosity=Sum("runreconstruction__run__recorded_lumi", output_field=FloatField()),
                number_of_ls=Sum("runreconstruction__run__lumisections"),
                day=(ExtractWeekDay("date")),
            )
        )

        """
        Add List of run_numbers per day and type to the summary
        """
        for d in summary_dict:
            runs = self.filter(
                date=d.get("date"),
                runreconstruction__run__run_type=d.get("runreconstruction__run__run_type"),
                runreconstruction__reconstruction=d.get("runreconstruction__reconstruction"),
            ).order_by("runreconstruction__run__run_number")
            run_numbers = [run.run_number for run in runs]
            d.update({"run_numbers": self.compare_list_if_certified(run_numbers)})

        return summary_dict

    def compare_list_if_certified(self, list_of_run_numbers):
        """
        :param list_of_run_numbers: list of run_numbers e.g. [317696, 123456, 317696, 317696]
        :type list_of_run_numbers: list
        :return: dictionary of run_numbers
        :rtype: dictionary {"good": [], "bad": [], "missing": [], "conflicting": []}
        """

        d = {"good": [], "bad": [], "missing": [], "different_flags": []}

        runs = self.annotate_status()

        cleaned_run_number_list = [
            i for i in list_of_run_numbers if type(i) == int or i.isdigit()
        ]

        changed_flag_runs = runs.filter(
            runreconstruction__run__run_number__in=cleaned_run_number_list
        ).filter_flag_changed()

        for run_number in list_of_run_numbers:
            try:
                run = runs.get(runreconstruction__run__run_number=run_number)
                d["{}".format(run.status)].append(run_number)
            except (ObjectDoesNotExist, ValueError):
                d["missing"].append(run_number)
            except MultipleObjectsReturned:
                run_pair = changed_flag_runs.filter(runreconstruction__run__run_number=run_number)
                if run_pair.exists():
                    d["different_flags"].append(run_number)
                else:
                    r = runs.filter(runreconstruction__run__run_number=run_number)
                    d["{}".format(r[0].status)].append(run_number)

        return d

    def changed_flags(self):
        """
        compares all run_numbers in current QuerySet against whole database
        and returns a list of run_numbers where the flags changed

        Example: Run was certified good in express and bad promptreco
        """
        return list(set([run.runreconstruction.run.run_number for run in self.filter_flag_changed()]))

    def today(self): # pragma: no cover
        pass

    def this_week(self): # pragma: no cover
        """
        filters QuerySet to only show runs of the current week
        week starts on monday at 00:00:00 and ends on sunday at 23:59:59
        """
        pass

    def last_week(self): # pragma: no cover
        """
        filters QuerySet to only show runs of the current week
        week starts on monday at 00:00:00 and ends on sunday at 23:59:59
        """
        pass

    def calendar_week(self, week_number): # pragma: no cover
        """
        filters QuerySet to only show runs of the specified calendar week

        A week starts on a monday. The week of a year that contains the first
        Thursday has the week number 1

        :param week_number: Week number according to the ISO-8601 standard.
        """
        pass

    def collisions(self):
        return self.filter(runreconstruction__run__run_type="collisions")

    def cosmics(self):
        return self.filter(runreconstruction__run__run_type="cosmics")

    def express(self):
        return self.filter(runreconstruction__reconstruction="express")

    def prompt(self):
        return self.filter(runreconstruction__reconstruction="prompt")

    def rereco(self):
        return self.filter(runreconstruction__reconstruction="rereco")

    def online(self): # pragma: no cover
        return self.filter(runreconstruction__reconstruction="online")

    def run_numbers(self):
        """
        :return: sorted list of run numbers (without duplicates)
        """
        return list(
            self.values_list("runreconstruction__run__run_number", flat=True).order_by("runreconstruction__run__run_number")
        )

    def fill_numbers(self):
        """
        :return: sorted list of fill numbers (without duplicates)
        """
        if not self.run_numbers():
            return []
        
        runs = runregistry.get_runs(filter={
           'run_number':{
              'or': self.run_numbers()
            }
        })
        fill_numbers_list = sorted(set({run["oms_attributes"]["fill_number"] for run in runs if run["oms_attributes"]["fill_number"] is not None}))
        return fill_numbers_list

    def pks(self):
        """
        :return: sorted list of primary keys
        """
        return list(self.values_list("pk", flat=True).order_by("pk"))

    def integrated_luminosity(self):
        if len(self) == 0:
            return 0
        print()
        return float(self.aggregate(runreconstruction__run__recorded_lumi__sum=Coalesce(Sum("runreconstruction__run__recorded_lumi"),0.0))["runreconstruction__run__recorded_lumi__sum"])

    def lumisections(self):
        if len(self) == 0:
            return 0
        return self.aggregate(Sum("runreconstruction__run__lumisections"))["runreconstruction__run__lumisections__sum"]

    def total_number(self):
        return len(self)

    def days(self):
        return [
            d["date"].strftime("%Y-%m-%d")
            for d in self.order_by("date").values("date").distinct()
        ]

    def reference_run_numbers(self):
        ref_dict = (
            self.order_by("reference_runreconstruction__run__run_number")
                .values("reference_runreconstruction__run__run_number")
                .distinct()
        )

        return [ref["reference_runreconstruction__run__run_number"] for ref in ref_dict]

    def runs(self):
        from certifier.models import RunReconstruction

        ref_ids = self.values_list("reference_runreconstruction", flat=True).order_by("reference_runreconstruction")
        return RunReconstruction.objects.filter(pk__in=ref_ids)

    def reference_runs(self):
        from certifier.models import RunReconstruction

        ref_ids = self.values_list("reference_runreconstruction", flat=True).order_by("reference_runreconstruction")
        return RunReconstruction.objects.filter(Q(pk__in=ref_ids) & Q(is_reference=True))

    def types(self):
        from certifier.models import TrackerCertification

        type_ids = self.values("runreconstruction__run__run_type", "runreconstruction__reconstruction").order_by("runreconstruction__run__run_type").distinct()

        return type_ids

    def per_day(self):
        """values_list
        Returns a list of querysets where one queryset is a specific day
        """
        per_day_list = []
        for day in self.days():
            per_day_list.append(self.filter(date=day))

        return per_day_list

    def per_type(self):
        """
        :return: list of querysets with one type per queryset
        """
        return [self.filter(Q(runreconstruction__run__run_type=t["runreconstruction__run__run_type"]) & Q(runreconstruction__reconstruction=t["runreconstruction__reconstruction"])) for t in self.types()]

    def trackermap_missing(self):
        return self.filter(trackermap="Missing")

    def shifters(self):
        """
        :return: list of users (shifters) in the queryset
        """
        user_ids = list(
            self.values_list("user", flat=True).order_by("user").distinct()
        )

        return get_user_model().objects.filter(pk__in=user_ids)

    def week_number(self):
        """
        :return: string of the week number(s) the runs were certified in
        """
        if not self.exists():
            return ""
        min_week = self.aggregate(Min("date"))["date__min"].isocalendar()[1]
        max_week = self.aggregate(Max("date"))["date__max"].isocalendar()[1]
        if min_week != max_week:
            return "{}-{}".format(min_week, max_week)
        return min_week

    def order_by_run_number(self):
        return self.order_by("runreconstruction__run__run_number")

    def order_by_date(self):
        return self.order_by("date", "runreconstruction__run__run_number")

    def print(self):
        """
        Prints out QuerySet to have an easy Overview
        """
        print()
        print(
            "{:10} {:10} {:10} {:10} {:10} {:10}".format(
                "run number", "type", "reco", "int lumi", "date", "flag"
            )
        )
        for run in self.annotate_status()[:50]:
            print(
                "{:10} {:10} {:10} {:10} {} {:10}".format(
                    run.runreconstruction.run.run_number,
                    run.runreconstruction.run.run_type,
                    run.runreconstruction.reconstruction,
                    run.runreconstruction.run.recorded_lumi,
                    run.date,
                    run.status,
                )
            )

    def print_verbose(self):
        """
        Prints out QuerySet to have an easy Overview
        """
        print(
            "{:<10} {:<10} {:<10} {:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} "
            "{:<10} {:<10}".format(
                "run number",
                "run type",
                "reco",
                "reference run",
                "trackermap",
                "lumisec",
                "int lumi",
                "pixel",
                "sistrip",
                "tracking",
                "date",
                "user",
            )
        )

        for run in self.annotate_status()[:50]:
            print(
                "{:<10} {:<10} {:<10} {:<30} {:<10} {:<10} {:<10} {:<10} {:<10} "
                "{:<10} {} {}".format(
                    run.runreconstruction.run.run_number,
                    run.runreconstruction.run.run_type,
                    run.runreconstruction.reconstruction,
                    "{} {} ({})".format(
                        run.reference_runreconstruction.run.run_type,
                        run.reference_runreconstruction.reconstruction,
                        run.reference_runreconstruction.run.run_number,
                    ),
                    run.trackermap,
                    run.runreconstruction.run.lumisections,
                    run.runreconstruction.run.recorded_lumi,
                    run.pixel,
                    run.strip,
                    run.tracking,
                    run.date,
                    run.user,
                )
            )

    def print_runs(self):
        for run in self.runs():
            print(
                "{:10} {:10} {:10} {:10} {:10}".format(
                    run.run.run_type,
                    run.reconstruction,
                    run.run.b_field,
                    run.run.fill_type_party1,
                    run.run.energy,
                )
            )

    def print_reference_runs(self):
        for ref in self.reference_runs():
            print(
                "{:10} {:10} {:10} {:10} {:10} {:10}".format(
                    ref.run.run_number,
                    ref.run.run_type,
                    ref.reconstruction,
                    ref.run.b_field,
                    ref.run.fill_type_party1,
                    ref.run.energy,
                )
            )

    def compare_with_run_registry(self):
        run_numbers = self.run_numbers()
        keys = [
            "runreconstruction__run__run_number",
            "runreconstruction__run__run_type",
            "runreconstruction__reconstruction",
            "pixel",
            "strip",
            "tracking",
        ]

        run_info_tuple_set = set(self.values_list(*keys))

        if not run_numbers: 
            return [], []

        run_registry_entries = runregistry.get_datasets(
            filter={
                    'run_number': {'or': run_numbers},
                    'dataset_name': { 'notlike': '%online%'}
                }
            )

        convert_run_registry_to_trackercertification(run_registry_entries)
        run_registry_tuple_set = {
            tuple(d[key] for key in keys) for d in run_registry_entries
        }

        deviating_run_info_tuple_list = sorted(
            run_info_tuple_set - run_registry_tuple_set
        )
        corresponding_run_registry_runs = []
        for run in deviating_run_info_tuple_list:
            elements = list(
                filter(
                    lambda x: x[0] == run[0] and x[2] == run[2], run_registry_tuple_set
                )
            )
            if not elements:
                elements = [("", "", "", "", "", "", False, False, False)]
            corresponding_run_registry_runs.extend(elements)

        deviating_run_info_dict = [
            dict(zip(keys, run)) for run in deviating_run_info_tuple_list
        ]
        corresponding_run_registry_dict = [
            dict(zip(keys, run)) for run in corresponding_run_registry_runs
        ]

        return deviating_run_info_dict, corresponding_run_registry_dict

    def matches_with_run_registry(self):
        deviating, corresponding = self.compare_with_run_registry()
        return len(deviating) == 0
    

    def group_run_numbers_by_fill_number(self):
        run_numbers = self.run_numbers()
        response = []
        runs = runregistry.get_runs(filter={
           'run_number':{
              'or': run_numbers
            }
        })

        for run in runs:
            response.append([run["oms_attributes"]["fill_number"],run["run_number"]])

        groups = groupby(response, itemgetter(0))
        items = [(key, [item[1] for item in value]) for key, value in groups]
        keys = ["fill_number", "run_number"]
        fill_run_group = [dict(zip(keys, item)) for item in items]
        return fill_run_group

    '''
    def annotate_fill_number(self):
        """
        Adds the lhc fill number from the Run Registry

        :return: QuerySet with added LHC fill number
        """
        run_registry = TrackerRunRegistryClient()
        fills = run_registry.get_fill_number_by_run_number(self.run_numbers())
        for run in self:
            fills_list=list(
                filter(lambda x: x["run_number"] == run.run_number, fills)
            )
            if(fills_list):
                run.fill_number = fills_list[0]["fill_number"]
    '''
