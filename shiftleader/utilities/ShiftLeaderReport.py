from shiftleader.utilities.utilities import to_weekdayname


class ShiftLeaderReportBase:
    """
    Base class for the shift leader report
    Just wraps the RunInfoQuerySet filter functions
    """
    def online(self): # pragma: no cover
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
    def __init__(self, runs):
        self.runs = runs
        try:
            day = runs[0].date
            self.day_name = to_weekdayname(day)
            self.day_date = day
        except IndexError:
            pass

    def name(self):
        return self.day_name

    def date(self):
        return self.day_date

    def flag_changed(self):
        runs = self.runs.filter_flag_changed(until=self.day_date)
        return type(self)(runs)


class ShiftLeaderReport(ShiftLeaderReportBase):
    def __init__(self, runs):
        self.runs = runs

    def day_by_day(self):
        return [ShiftLeaderReportDay(day) for day in self.runs.per_day()]
