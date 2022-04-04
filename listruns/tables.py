import django_tables2 as tables
from certifier.models import TrackerCertification, RunReconstruction
from listruns.utilities.luminosity import format_integrated_luminosity
from listruns.utilities.tables import render_component, render_trackermap


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
    comment = tables.TemplateColumn(
        '<div id="id_comment">'
        '{{record.comment}}'
        '</div>', )
    date = tables.Column()

    class Meta:
        model = TrackerCertification
        fields = ()
        attrs = {"class": "table table-hover table-bordered table-fixed"}

    def render_reference_run(self, value):  # pragma: no cover
        """
        :return: run number of the reference run
        """
        return value.reference_runreconstruction

    def render_int_luminosity(self, value):  # pragma: no cover
        """
        :return: unit aware integrated luminosity e.g. '1.321 µb⁻¹'
        """
        return format_integrated_luminosity(value)

    def render_pixel(self, record):  # pragma: no cover
        """
        :return: colored status of Pixel
        """
        return render_component(record.pixel, record.pixel_lowstat)

    def render_strip(self, record):  # pragma: no cover
        """
        :return: colored status of Strip
        """
        return render_component(record.strip, record.strip_lowstat)

    def render_tracking(self, record):  # pragma: no cover
        """
        :return: colored status of Tracking
        """
        return render_component(record.tracking, record.tracking_lowstat)

    def render_trackermap(self, value):  # pragma: no cover
        """
        :return: colored status of the tracker map
        """
        return render_trackermap(value)


class TrackerCertificationTable(SimpleTrackerCertificationTable):
    """
    TrackerCertification table used by shifters
    """
    is_reference = tables.Column(verbose_name="Is Reference",
                                 accessor="runreconstruction.is_reference")

    edit_run = tables.TemplateColumn(
        '<div align="center">'
        '<a href="{% url \'listruns:update\' pk=record.pk run_number=record.runreconstruction.run.run_number reco=record.runreconstruction.reconstruction%}">'
        '{% if user == record.user or user.has_shift_leader_rights %}'
        '<button class="btn btn-block btn-danger" id="id_certificaion_update">'
        '{% else %}'
        '<button class="btn btn-block btn-danger" id="id_certificaion_update" disabled>'
        '{% endif %}'
        'Edit'
        '</button>'
        '</a>'
        '</div>',
        orderable=False,
        verbose_name="Edit",
    )

    class Meta:
        attrs = {"class": "table table-hover table-bordered table-fixed"}
