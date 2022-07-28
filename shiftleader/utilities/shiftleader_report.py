import logging
from certifier.query import TrackerCertificationQuerySet
from shiftleader.utilities.utilities import to_weekdayname

logger = logging.getLogger(__name__)


class ShiftLeaderReportBase:
    """
    Base class for the shift leader report
    Just wraps the TrackerCertificationQuerySet filter functions.

    Each of the methods returns a *new* ShiftLeaderReport
    instance, instanciated with a more filtered queryset.

    e.g., the code below:

    ```
    s = ShiftLeaderReport(TrackerCertification.objects.all())
    s = s.collisions().express()
    ```

    will return a new ShiftLeaderReport, where the queryset
    is limited to the TrackerCertifications of express collisions.
    """

    def __init__(self, runs: TrackerCertificationQuerySet, *args, **kwargs):
        self.runs = runs

    def online(self):  # pragma: no cover
        return type(self)(self.runs.online())

    def prompt(self):
        return type(self)(self.runs.prompt())

    def express(self):
        return type(self)(self.runs.express())

    def rereco(self):
        return type(self)(self.runs.rereco())

    def collisions(self):
        return type(self)(self.runs.collisions())

    def cosmics(self):
        return type(self)(self.runs.cosmics())

    def bad(self):
        return type(self)(self.runs.bad())

    def good(self):
        return type(self)(self.runs.good())

    def run_numbers(self):
        return self.runs.run_numbers()

    def fill_numbers(self):
        return self.runs.fill_numbers()

    def fills(self):
        return self.runs.group_run_numbers_by_fill_number()

    def integrated_luminosity(self):
        return self.runs.integrated_luminosity()

    def total_number(self):
        return self.runs.total_number()


class ShiftLeaderReportDay(ShiftLeaderReportBase):
    def __init__(self, runs, *args, **kwargs):
        try:
            day = runs[0].date
            self.day_name = to_weekdayname(day)
            self.day_date = day
        except IndexError:
            pass
        super().__init__(runs, *args, **kwargs)

    def name(self):
        return self.day_name

    def date(self):
        return self.day_date

    def flag_changed(self):
        runs = self.runs.filter_flag_changed(until=self.day_date)
        return type(self)(runs)


class ShiftLeaderReport(ShiftLeaderReportBase):
    def __init__(self, runs, *args, **kwargs):
        super().__init__(runs, *args, **kwargs)

    def day_by_day(self):
        return [ShiftLeaderReportDay(day) for day in self.runs.per_day()]
