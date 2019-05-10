from django import template

register = template.Library()

@register.inclusion_tag('checklists/checklists/checklist_checkbox.html')
def render_checklist_checkbox(form_checklist, label="", not_required=False): #pragma: no cover
    """"
    renders a Checklist checkbox with a label

    Example Usage:
    {% render_checklist_checkbox form.checklists.general %}
    """
    try:
        if not label:
            label = form_checklist["checklist"].title + " Checklist"

        context = {
            'checklist': form_checklist["checklist"],
            'checkbox': form_checklist["field"],
            'label': label
        }

        if not not_required:
            context['required'] = True

        return context
    except TypeError:
        # Don't render if no checklist is provided
        return {}


@register.inclusion_tag('checklists/checklists/checklist_modal.html')
def render_checklist_modal(form_checklist, label=""): #pragma: no cover
    """"
    renders a Checkbox and a Modal

    Example Usage:
    {% render_checklist_modal form.checklists.trackermap %}
    """
    try:
        checklist = form_checklist["checklist"]
        checkbox = form_checklist["field"]
        if not label:
            label = checklist.title + " Checklist"
        return {'checklist': checklist, 'checkbox': checkbox, 'label': label}
    except TypeError:
        # Don't render if no checklist is provided
        return {}
