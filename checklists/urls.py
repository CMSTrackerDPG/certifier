from django.urls import path

from . import views

app_name='checklists'
urlpatterns = [
    path(
        "checklists/general$",
        ChecklistTemplateView.as_view(
            template_name="checklists/templates/checklists/html/general.html"
        ),
        name="general_checklist",
    ),
    path(
        "checklists/trackermap$",
        ChecklistTemplateView.as_view(
            template_name="checklists/templates/checklists/html/trackermap.html"
        ),
        name="trackermap_checklist",
    ),
    path(
        "checklists/pixel$",
        ChecklistTemplateView.as_view(template_name="checklists/templates/checklists/html/pixel.html"),
        name="pixel_checklist",
    ),
    path(
        "checklists/sistrip$",
        ChecklistTemplateView.as_view(
            template_name="checklistsi/templates/checklists/html/sistrip.html"
        ),
        name="sistrip_checklist",
    ),
    path(
        "checklists/tracking$",
        ChecklistTemplateView.as_view(
            template_name="checklists/templates/checklists/html/tracking.html"
        ),
        name="tracking_checklist",
    ),
]
