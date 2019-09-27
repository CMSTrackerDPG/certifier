from django.utils.safestring import mark_safe
from certifier.models import TrackerCertification


def render_component(component, component_lowstat): # pragma: no cover
    """
    Renders the component (Pixel/ SiStrip/ Tracking) for the TrackerCertificationTable

    If lowstat is checked then "Lowstat" is displayed instead of Good/Bad/Excluded
    If the Component is good, then the color will be green, otherwise red.

    This should lead to a similar behavior as in the RunRegistry
    """
    component_rating = component.lower()
    css_class = None

    if component_rating == "good" or component_rating == "lowstat":
        css_class = "good-component"
    elif component_rating == "bad":
        css_class = "bad-component"
    elif component_rating == "excluded":
        css_class = "excluded-component"

    component_value = component

    if component_lowstat is True and component_rating != "excluded":
        component_value = "Lowstat"

    if css_class:
        return mark_safe(
            '<div class="{}">{}</div>'.format(css_class, component_value.title())
        )
    return component

def render_certify_button(run_number, dataset_express, dataset_prompt, dataset_rereco):
    css_class = None

    if TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number, runreconstruction__reconstruction="express").exists()\
    and TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number, runreconstruction__reconstruction="prompt").exists()\
    and TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number, runreconstruction__reconstruction="rereco").exists():
        return mark_safe(
            '<div align="center">'
                    '<button class="btn btn-info" disabled>{}</button>'
            '</div>'.format("Certified")
            )
    else:
        return mark_safe(
            '<div align="center">'
                '<a href="\certify\{}">'
                    '<button class="btn btn-info">'
                        'Certify'
                    '</button>'
                '</a>'
            '</div>'.format(run_number)
                )


def render_dataset(run_number, dataset, reco): # pragma: no cover
    css_class = None

    if TrackerCertification.objects.filter(runreconstruction__run__run_number=run_number, runreconstruction__reconstruction=reco).exists():
        css_class = "good-dataset"

    if css_class:
        return mark_safe(
            '<div class="{}">{}</div>'.format(css_class, dataset)
        )

    return mark_safe(
        '<div>{}</div'.format(dataset)
    )


def render_trackermap(trackermap): # pragma: no cover
    if trackermap == "Missing":
        return mark_safe('<div class="bad-component">{}</div>'.format(trackermap))
    return trackermap


def render_boolean_cell(value): # pragma: no cover
    boolean_value = False if value is False or value == "0" or value == 0 else True
    print("{} {}".format(value, boolean_value))
    glyphicon = "ok" if boolean_value else "remove"

    html = '<span class="glyphicon glyphicon-{}"></span>'.format(glyphicon, glyphicon)

    return mark_safe(html)

