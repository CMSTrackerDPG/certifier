from .models import Checklist
from django import forms

class ChecklistFormMixin(forms.Form):
    """
    Adds mandatory Checklist checkboxes to the form
    E.g. general, trackermap, sistrip, pixel, tracking

    Form can only be submitted when all the checkboxes have been ticked

    Whether the checkbox is ticked or not is just checked client-side (html)
    and NOT server-side.

    Example Usage:
    form.checklist_sistrip -> renders the SiStrip Checklist checkbox
    """

    def __init__(self, *args, **kwargs): #pragma: no cover
        super(ChecklistFormMixin, self).__init__(*args, **kwargs)
        for checklist in Checklist.objects.all():
            field_name = "checklist_{}".format(checklist.identifier)
            # required in HTML field, not required in server-side form validation
            self.fields[field_name] = forms.BooleanField(required=False)

    def checklists(self): #pragma: no cover
        """
        returns a dictionary containing the fields (checkboxes) created in the __init__
        method and the corresponding Checklist model instances

        Example Usage:
        form.checklists.pixel.field -> returns the rendered Checklist checkbox
        form.checklists.pixel.checklist -> returns the Checklist model instance
        """
        checklist_list = {}  # List of checklists containing their checkbox items
        for checklist in Checklist.objects.all():
            field_name = "checklist_{}".format(checklist.identifier)
            checklist_list.update({
                checklist.identifier: {
                    "checklist": checklist,
                    "field": self[field_name]
                }})
        return checklist_list

