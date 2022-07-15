from django import forms
from oms.models import OmsRun, OmsFill


class OmsRunForm(forms.ModelForm):
    class Meta:
        model = OmsRun
        template_name = "oms/omsrun_form.html"
        # Not adding "fill" in fields, since it
        # will be manually updated after POST
        fields = [
            "run_type",
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
        ]


class OmsFillForm(forms.ModelForm):
    class Meta:
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
