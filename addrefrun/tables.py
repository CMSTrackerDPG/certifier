import django_tables2 as tables
from certifier.models import RunReconstruction


class SimpleRunReconstructionTable(tables.Table):
    """
    A table to render RunReconstruction entries, mainly used in the addrefrun app
    """
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

    def render_run(self, value):  # pragma: no cover
        """
        :return: run number of the reference run
        """
        return value.run_number
