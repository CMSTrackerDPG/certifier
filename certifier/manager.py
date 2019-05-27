from decimal import Decimal

from django.db import models

from shiftleader.query import TrackerCertificationQuerySet
from certifier.utilities.utilities import uniquely_sorted
from delete.manager import SoftDeletionManager

class TrackerCertificationManager(SoftDeletionManager):
    def get_queryset(self):
        if self.alive_only:
            return TrackerCertificationQuerySet(self.model).filter(deleted_at=None)
        return TrackerCertificationQuerySet(self.model)

    def good(self):
        return TrackerCertificationQuerySet(self.model).good()

    def bad(self):
        return TrackerCertificationQuerySet(self.model).bad()

    def check_if_certified(self, list_of_run_numbers):
        list_of_run_numbers = uniquely_sorted(list_of_run_numbers)

        # TODO use self.get_queryset() instead of TrackerCertificationQuerySet(self.model).filter
        runs = TrackerCertificationQuerySet(self.model).filter(deleted_at=None)
        runs = runs.filter(run_number__in=list_of_run_numbers).annotate_status()

        def do_check(runs):
            flags = {
                "good": [],
                "bad": [],
                "missing": [],
                "prompt_missing": [],
                "changed_good": [],  # Express Bad -> Prompt Good
                "changed_bad": [],  # Express Good -> Prompt Bad
            }

            prompt_runs = runs.prompt()
            good_runs = prompt_runs.good()
            bad_runs = prompt_runs.bad()

            flags["good"] = good_runs.run_numbers()
            flags["bad"] = bad_runs.run_numbers()

            non_missing_prompt_run_numbers = [
                run["run_number"] for run in prompt_runs
                    .order_by("run_number")
                    .values("run_number")
                    .distinct()
            ]

            non_missing_run_numbers = [
                run["run_number"] for run in runs
                    .order_by("run_number")
                    .values("run_number")
                    .distinct()
            ]

            flags["prompt_missing"] = list(
                set(non_missing_run_numbers) - set(non_missing_prompt_run_numbers))

            express_runs = runs.express().filter(run_number__in=non_missing_run_numbers)
            good_express = express_runs.good().run_numbers()
            bad_express = express_runs.bad().run_numbers()

            for run in good_express:
                if run in flags["bad"]:
                    flags["bad"].remove(run)
                    flags["changed_bad"].append(run)

            for run in bad_express:
                if run in flags["good"]:
                    flags["good"].remove(run)
                    flags["changed_good"].append(run)

            for d in flags.values():
                d.sort()
            return flags

        check_dictionary = {
            "collisions": do_check(runs.collisions()),
            "cosmics": do_check(runs.cosmics())
        }

        non_missing_run_numbers = []

        for key, dic in check_dictionary.items():
            for key, value in dic.items():
                for run_number in value:
                    non_missing_run_numbers.append(run_number)

        check_dictionary["missing"] = list(
            (set(list_of_run_numbers) - set(non_missing_run_numbers))
        )

        return check_dictionary

    def check_integrity_of_run(self, trackerCertification):
        """
        Checks if the given run is consistent with existing runs.

        For example, if a collisions express run with the run number 333333 was
        certified then the collisions prompt run with the same run number should have
        the same runtype, bfield, energy, number_of_ls, int_lumi, ...

        Also in most cases the components pixel, sistrip, tracking should match,
        but can vary from time to time. If they vary then the shifter should double
        check that this is what he intended.

        :param run: RunInfo instance
        :return: dictionary containing the mismatches and the counterpart value.
        empty means no mismatch.
        """

        from certifier.models import TrackerCertification
        try:
            if trackerCertification.runreconstruction.reconstruction == "reReco":
                return {}
        except Type.DoesNotExist:
            # No Type selected yet
            return {}

        type_attributes_to_be_checked = [
            "runreconstruction__run__run_type",
            "runreconstruction__run__b_field",
            "runreconstruction__run__fill__fill_type_runtime",  # "beamenergy",
        ]
        run_attributes_to_be_checked = [
            "runreconstruction__run__lumisections",
            "pixel",
            "strip",
            "tracking",
            "pixel_lowstat",
            "strip_lowstat",
            "tracking_lowstat"
        ]
        decimal_attributes_to_be_checked = [
            "int_luminosity",
        ]

        mismatches = {}

        try:
            counterpart_reco = "Express" if trackerCertification.runreconstruction.reconstruction == "Prompt" else "Prompt"

            counterpart_run = self.get_queryset().get(
                run_number=trackerCertification.runreconstruction.run_number,
                runreconstruction__reconstruction=counterpart_reco
            )

            counterpart_type = counterpart_run.run.run_type
            assert counterpart_run.reconstruction != run.type.reco

            mismatches.update({
                attribute: getattr(counterpart_type, attribute)
                for attribute in type_attributes_to_be_checked
                if getattr(run.type, attribute) is not None and
                   getattr(counterpart_type, attribute) != getattr(run.type, attribute)
            })

            mismatches.update({
                attribute: getattr(counterpart_run, attribute)
                for attribute in run_attributes_to_be_checked
                if getattr(run, attribute) is not None and
                   getattr(counterpart_run, attribute) != getattr(run, attribute)
            })

            mismatches.update({
                attribute: getattr(counterpart_run, attribute)
                for attribute in decimal_attributes_to_be_checked
                if getattr(run, attribute) is not None and
                    abs(
                        getattr(counterpart_run, attribute) - getattr(run, attribute)
                    ) > Decimal("0.1")
            })

            return mismatches
        except TrackerCertification.DoesNotExist:
            # No counterpart means no mismatch
            return {}
