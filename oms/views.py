from django.views.generic.edit import UpdateView
from oms.models import OmsRun, OmsFill


class OmsRunUpdateView(UpdateView):
    model = OmsRun
    template_name = "oms/omsrun_form.html"
    fields = ["run_type", "fill"]
