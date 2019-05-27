from django import template

register = template.Library()

@register.inclusion_tag('shiftleader/label_and_field.html')
def render_label_and_field_for(field):
    return {'field': field}

@register.inclusion_tag('shiftleader/lhc_fill_table.html')
def render_lhc_fill_table(queryset, caption):
    return {"queryset": queryset, "caption": caption}
