from django.shortcuts import render

# Create your views here.

# TODO update Checklist by Checklist model, return 404 if page doesnt exist
class ChecklistTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist_base_template_name"] = "certhelper/checklists/base.html"
        return context
