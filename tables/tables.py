import django_tables2 as tables
from django.utils.safestring import mark_safe

from tables.utilities.utilities import (
    render_component,
    render_trackermap,
    render_boolean_cell,
    render_dataset,
    render_certify_button,
)
from listruns.utilities.luminosity import format_integrated_luminosity
from certifier.models import TrackerCertification, RunReconstruction
from openruns.models import OpenRuns

class SimpleRunReconstructionTable(tables.Table):
    run = tables.Column(verbose_name="Run Number")
    reconstruction = tables.Column()
    run_type = tables.Column(accessor="run.run_type")
    is_reference = tables.Column()
    delete_run = tables.TemplateColumn(
        '<div align="center">'
        '<a href="{% url \'delete:delete_reference\' run_number=record.run.run_number reco=record.reconstruction%}">'
                'Delete'
            '</a>'
        '</div>',
        orderable=False,
        verbose_name="Delete",
    )

    class Meta:
        model = RunReconstruction
        fields = ()
        attrs = {"class": "table table-hover table-bordered table-fixed"}

    def render_run(self, value): # pragma: no cover
        """
        :return: run number of the reference run
        """
        return value.run_number

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
        '</div>',
    )
    date = tables.Column()

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
    is_reference = tables.Column(verbose_name="Is Reference", accessor="runreconstruction.is_reference")

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

    promote_run = tables.TemplateColumn(
        '<div align="center">'
            '<a href="{% url \'promote\' run_number=record.runreconstruction.run.run_number reco=record.runreconstruction.reconstruction%}">'
                'Promote'
            '</a>'
        '</div>',
        orderable=False,
        verbose_name="Promote to Reference",
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

    def render_pixel(self, record):  # pragma: no cover
        return render_component(record.get("pixel"), record.get("pixel_lowstat"))

    def render_strip(self, record):  # pragma: no cover
        return render_component(record.get("strip"), record.get("strip_lowstat"))

    def render_tracking(self, record):  # pragma: no cover
        return render_component(record.get("tracking"), record.get("tracking_lowstat"))

class OpenRunsTable(tables.Table):
    run_number = tables.Column(verbose_name="Run Number")
    user = tables.Column(verbose_name="User")

    dataset_express = tables.Column(verbose_name="Express")
    dataset_prompt = tables.Column(verbose_name="Prompt")
    dataset_rereco = tables.Column(verbose_name="ReReco")
    dataset_rereco_ul = tables.Column(verbose_name="ReRecoUL")

    certify = tables.TemplateColumn(
        '<div></div>',
        orderable=False,
        verbose_name="",
        visible=False
    )

    delete = tables.TemplateColumn(
        '<div align="center">'
            '<a href="{% url \'delete:delete_open_run\' run_number=record.run_number %}">'
            '{% if user == record.user or user.has_shift_leader_rights %}'
                '<button class="btn btn-block btn-danger" id="id_openruns_delete">'
            '{% else %}'
                '<button class="btn btn-block btn-danger" id="id_openruns_delete" disabled>'
            '{% endif %}'
                'Remove Entry'
                '</button>'
            '</a>'
        '</div>',
        orderable=False,
        verbose_name=""
    )

    def render_run_number(self, record): # pagman: no cover
        return mark_safe(
            '<div>'
                '<span class="align-middle">{}</span>'
            '</div>'.format(record.run_number),
        )

    def render_dataset_express(self, record): # pragma: no cover
        """
        :return: colored status of Dataset
        """
        return render_dataset(record.run_number ,record.dataset_express, record.state_express, "express", record.user, self.request.user)

    def render_dataset_prompt(self, record): # pragma: no cover
        """
        :return: colored status of Dataset
        """
        return render_dataset(record.run_number, record.dataset_prompt, record.state_prompt, "prompt", record.user, self.request.user)

    def render_dataset_rereco(self, record): # pragma: no cover
        """
        :return: colored status of Dataset
        """
        return render_dataset(record.run_number, record.dataset_rereco, record.state_rereco, "rereco", record.user, self.request.user)

    def render_dataset_rereco_ul(self, record): # pragma: no cover
        """
        :return: colored status of Dataset
        """
        return render_dataset(record.run_number, record.dataset_rereco_ul, record.state_rereco_ul, "rerecoul", record.user, self.request.user)

    def render_certify(self, record): # pragma: no cover
        """
        :return: colored Certify button
        """
        return render_certify_button(record.run_number, record.dataset_express, record.dataset_prompt, record.dataset_rereco)

    class Meta:
        attrs = {
            "class": "table table-stripped",
            "id": "openruns_table"
            }
        row_attrs = {
                'user_row': lambda record: record.user.username
            }
