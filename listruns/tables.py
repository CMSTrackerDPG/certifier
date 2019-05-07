import django_tables2 as tables

from listruns.utilities.utilities import (
    render_component,
    render_trackermap,
    render_boolean_cell,
)
from listruns.utilities.luminosity import format_integrated_luminosity
from certifier.models import TrackerCertification


class SimpleTrackerCertificationTable(tables.Table):
    """
    Simple readonly TrackerCertification table without any edit/ delete buttons
    """

    user = tables.Column(verbose_name="Shifter")
    runreconstruction = tables.Column()
    reference_runreconstruction = tables.Column()
    trackermap = tables.Column()
    pixel = tables.Column()
    strip = tables.Column()
    tracking = tables.Column()
    comment = tables.Column()
    date = tables.Column()
    pixel_problems = tables.Column()
    strip_problems = tables.Column()
    tracking_problems = tables.Column()

    class Meta:
        model = TrackerCertification
        fields = ()
        attrs = {"class": "table table-hover table-bordered table-fixed"}

    def render_reference_run(self, value):
        """
        :return: run number of the reference run
        """
        return value.reference_runreconstruction

    def render_int_luminosity(self, value):
        """
        :return: unit aware integrated luminosity e.g. '1.321 µb⁻¹'
        """
        return format_integrated_luminosity(value)

    def render_pixel(self, record):
        """
        :return: colored status of Pixel
        """
        return render_component(record.pixel, record.pixel_lowstat)

    def render_strip(self, record):
        """
        :return: colored status of Strip
        """
        return render_component(record.strip, record.strip_lowstat)

    def render_tracking(self, record):
        """
        :return: colored status of Tracking
        """
        return render_component(record.tracking, record.tracking_lowstat)

    def render_trackermap(self, value):
        """
        :return: colored status of the tracker map
        """
        return render_trackermap(value)


class TrackerCertificationTable(SimpleTrackerCertificationTable):
    """
    TrackerCertification table used by shifters
    """

    edit_run = tables.TemplateColumn(
        '<div align="center"><a href="{% url \'listruns:update\' pk=record.pk run_number=record.runreconstruction.run.run_number reco=record.runreconstruction.reconstruction%}">'
        '<span>Edit</a></div>',
        orderable=False,
        verbose_name="Edit",
    )

    class Meta:
        attrs = {"class": "table table-hover table-bordered table-fixed"}
