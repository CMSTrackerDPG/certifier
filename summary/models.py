from django.db import models
from django.contrib.postgres.fields import ArrayField
from summary.validators import validate_list_length


class SummaryInfo(models.Model):
    """
    Information regarding a summary/Elog.

    A summary is identified by the list of runs it is composed of
    """

    runs = ArrayField(
        base_field=models.IntegerField(null=False),
        help_text="Unique summary for list of runs",
        unique=True,
    )
    links_prompt_feedback = models.TextField(
        help_text="tinyurl links to plots on cmsweb.cern.ch"
    )
    special_comment = models.TextField(
        help_text="Special comment by shifter for this summary"
    )

    def save(self, *args, **kwargs):
        # ArrayField does not seem to use a validators argument
        validate_list_length(self.runs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__} {self.runs}"
