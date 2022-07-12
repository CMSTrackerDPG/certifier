from summary.utilities.utilities import get_ascii_table
from listruns.utilities.luminosity import format_integrated_luminosity
from certifier.models import TrackerCertification


class SummaryReport:
    """
    SummaryReport used in summary.html.
    Everything is returned per type.
    """

    def __init__(self, runs):
        self.runs = runs
        self.runs_per_type = runs.per_type()

    def reference_runs(self):
        return self.runs.reference_runs()

    def runs_checked_per_type(self):
        runs_checked = []

        for idx, certs_with_specific_type in enumerate(self.runs_per_type):
            column_description = [
                "Run",
                "Reference Run",
                "Number of LS",
                "Int. Luminosity",
                "Tracking",
                "Pixel",
                "Strip",
                "Comment",
            ]

            data = [
                [
                    certification.runreconstruction.run.run_number,
                    certification.reference_runreconstruction.run.run_number,
                    certification.runreconstruction.run.lumisections,
                    format_integrated_luminosity(
                        certification.runreconstruction.run.recorded_lumi,
                        luminosity_units=certification.runreconstruction.run.recorded_lumi_unit,
                        to_ascii=True,
                    ),
                    certification.tracking,
                    certification.pixel,
                    certification.strip,
                    certification.comment,
                ]
                for certification in certs_with_specific_type
            ]

            headline = (
                "Type "
                + str(idx + 1)
                + ": "
                + str(certs_with_specific_type[0].runreconstruction.reconstruction)
                + " "
                + str(certs_with_specific_type[0].runreconstruction.run.run_type)
                + " "
                + str(certs_with_specific_type[0].runreconstruction.run.b_field)
                + " T "
                + str(
                    certs_with_specific_type[0].runreconstruction.run.fill_type_party1
                )
                + " "
                + str(certs_with_specific_type[0].runreconstruction.run.energy)
                + " TeV "
                + str(
                    TrackerCertification.objects.get(
                        runreconstruction=certs_with_specific_type[0]
                    ).dataset
                )
            )

            table = get_ascii_table(column_description, data)
            runs_checked.append(headline + "\n" + table + "\n")

        return runs_checked

    def tracker_maps_per_type(self):
        tracker_maps = []
        for idx, certs_with_specific_type in enumerate(self.runs_per_type):
            text = "Type {}".format(idx + 1)
            tk_map_exists_runs = certs_with_specific_type.filter(trackermap="exists")
            if tk_map_exists_runs.exists():
                run_numbers = tk_map_exists_runs.run_numbers()
                joined = " ".join(str(run_number) for run_number in run_numbers)
                text += "\n Exists: {}".format(joined)

            tk_map_missing_runs = certs_with_specific_type.filter(trackermap="missing")
            if tk_map_missing_runs.exists():
                run_numbers = tk_map_missing_runs.run_numbers()
                joined = " ".join(str(run_number) for run_number in run_numbers)
                text += "\n Missing: {}".format(joined)
            tracker_maps.append(text + "\n")
        return tracker_maps

    def certified_runs_per_type(self):
        certified_run_numbers = []
        for idx, certs_with_specific_type in enumerate(self.runs_per_type):
            text = "Type {}".format(idx + 1)
            good = certs_with_specific_type.good()
            if good.exists():
                run_numbers = good.run_numbers()
                joined = " ".join(str(run_number) for run_number in run_numbers)
                text += "\n Good: {}".format(joined)

            bad = certs_with_specific_type.bad()
            if bad.exists():
                run_numbers = bad.run_numbers()
                joined = " ".join(str(run_number) for run_number in run_numbers)
                text += "\n Bad: {}".format(joined)
            certified_run_numbers.append(text + "\n")
        return certified_run_numbers

    def sum_of_quantities_per_type(self):
        certified_run_numbers = []
        for idx, certs_with_specific_type in enumerate(self.runs_per_type):
            column_description = [
                "Type {}".format(idx + 1),
                "Sum of LS",
                "Sum of int. luminosity",
            ]

            data = []
            good = certs_with_specific_type.good()
            bad = certs_with_specific_type.bad()

            if good.exists():
                data.append(
                    [
                        "Good",
                        good.lumisections(),
                        format_integrated_luminosity(
                            good.integrated_luminosity(), to_ascii=True
                        ),
                    ]
                )

            if bad.exists():
                data.append(
                    [
                        "Bad",
                        bad.lumisections(),
                        format_integrated_luminosity(
                            bad.integrated_luminosity(), to_ascii=True
                        ),
                    ]
                )

            table = get_ascii_table(column_description, data)
            certified_run_numbers.append(table)
        return certified_run_numbers
