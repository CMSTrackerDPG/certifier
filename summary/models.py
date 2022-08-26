from django.db import models
from django.contrib.postgres.fields import ArrayField


class SummaryInfo(models.Model):
    """
    Information regarding a summary/Elog.

    A summary is identified by the list of runs it is composed of
    """

    runs = ArrayField(
        base_field=models.IntegerField(blank=False, null=False),
        primary_key=True,
        help_text="Unique summary for list of runs",
    )
    links_prompt_feedback = models.TextField(
        help_text="tinyurl links to plots on cmsweb.cern.ch"
    )
    special_comment = models.TextField(
        help_text="Special comment by shifter for this summary"
    )
