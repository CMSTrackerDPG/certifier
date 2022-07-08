from django.views.generic.edit import UpdateView
from oms.models import OmsRun, OmsFill


class OmsRunUpdateView(UpdateView):
    model = OmsRun
    template_name = "oms/omsrun_form.html"
    fields = [
        "run_type",
        "fill",
        "b_field",
        "b_field_unit",
        "lumisections",
        "recorded_lumi",
        "recorded_lumi_unit",
        "init_lumi",
        "init_lumi_unit",
        "delivered_lumi",
        "delivered_lumi_unit",
        "end_lumi",
        "end_lumi_unit",
        "energy",
        "energy_unit",
        # "era",
    ]


class OmsFillUpdateView(UpdateView):
    model = OmsFill
    template_name = "oms/omsfill_form.html"
    fields = [
        "fill_number",
        "fill_type_runtime",
        "era",
        "init_lumi",
        "init_lumi_unit",
        "peak_lumi",
        "peak_lumi_unit",
        "peak_pileup",
        "bunches_colliding",
    ]
