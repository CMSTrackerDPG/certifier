# Create your views here.
from django.views.generic import TemplateView

# TODO update Checklist by Checklist model, return 404 if page doesnt exist
class ChecklistTemplateView(TemplateView): #pragma: no cover
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist_base_template_name"] = "checklists/templates/checklists/html/base.html"
        return context
