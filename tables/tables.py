import django_tables2 as tables

from tables.utilities.utilities import (
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

    def render_reference_run(self, value): # pragma: no cover
        """
        :return: run number of the reference run
        """
        return value.reference_runreconstruction

    def render_int_luminosity(self, value): # pragma: no cover
        """
        :return: unit aware integrated luminosity e.g. '1.321 µb⁻¹'
        """
        return format_integrated_luminosity(value)

    def render_pixel(self, record): # pragma: no cover
        """
        :return: colored status of Pixel
        """
        return render_component(record.pixel, record.pixel_lowstat)

    def render_strip(self, record): # pragma: no cover
        """
        :return: colored status of Strip
        """
        return render_component(record.strip, record.strip_lowstat)

    def render_tracking(self, record): # pragma: no cover
        """
        :return: colored status of Tracking
        """
        return render_component(record.tracking, record.tracking_lowstat)

    def render_trackermap(self, value): # pragma: no cover
        """
        :return: colored status of the tracker map
        """
        return render_trackermap(value)


class TrackerCertificationTable(SimpleTrackerCertificationTable):
    """
    TrackerCertification table used by shifters
    """

    edit_run = tables.TemplateColumn(
        '<div align="center">'
            '<a href="{% url \'listruns:update\' pk=record.pk run_number=record.runreconstruction.run.run_number reco=record.runreconstruction.reconstruction%}">'
                'Edit'
            '</a>'
        '</div>',
        orderable=False,
        verbose_name="Edit",
    )

    class Meta:
        attrs = {"class": "table table-hover table-bordered table-fixed"}

class ShiftleaderTrackerCertificationTable(TrackerCertificationTable):
    """
    TrackerCertification table used by shift leaders
    """

    delete_run = tables.TemplateColumn(
        '<div align="center">'
            '<a href="{% url \'delete:delete\' pk=record.pk run_number=record.runreconstruction.run.run_number reco=record.runreconstruction.reconstruction%}">'
                'Delete'
            '</a>'
        '</div>',
        orderable=False,
        verbose_name="Delete",
    )

    class Meta:
        attrs = {"class": "table table-hover table-bordered"}


class DeletedTrackerCertificationTable(tables.Table):
    restore_run = tables.TemplateColumn(
        '<div align="center">'
            '<a href="{% url \'restore:restore_run\' pk=record.pk run_number=record.runreconstruction.run.run_number reco=record.runreconstruction.reconstruction%}">'
                'Restore'
            '</a>'
        '</div>',
        orderable=False,
    )

    delete_forever = tables.TemplateColumn(
        '<div align="center">'
            '<a href="{% url \'delete:hard_delete_run\' pk=record.pk run_number=record.runreconstruction.run.run_number reco=record.runreconstruction.reconstruction%}">'
                'Hard Delete'
            '</a>'
        '</div>',
        orderable=False,
    )

    class Meta:
        model = TrackerCertification
        fields = (
            "pk",
            "deleted_at",
            "user",
            "run_number",
            "reconstruction",
            "reference_runreconstruction",
            "date",
        )
        attrs = {"class": "table table-hover table-bordered"}

class RunRegistryComparisonTable(tables.Table):
    runreconstruction__run__run_number = tables.Column(verbose_name="Run Number")
    runreconstruction__run__run_type = tables.Column(verbose_name="Run Type")
    runreconstruction__reconstruction = tables.Column(verbose_name="Reco")
    pixel = tables.Column()
    strip = tables.Column()
    tracking = tables.Column()

    class Meta:
        attrs = {"class": "table table-hover table-bordered"}

    def render_pixel(self, record):
        return render_component(record.get("pixel"), record.get("pixel_lowstat"))

    def render_strip(self, record):
        return render_component(record.get("strip"), record.get("strip_lowstat"))

    def render_tracking(self, record):
        return render_component(record.get("tracking"), record.get("tracking_lowstat"))
