from django import template

register = template.Library()

@register.filter(name='translate_to_button_state')
def translate_to_button_state(status):
    if status == "good":
        return "success"
    elif status == "bad":
        return "danger"
    else:
        return "secondary"

@register.filter(name='slice_last_elem')
def slice(all_elem):
    return all_elem[:-1]
