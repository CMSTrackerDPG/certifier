import logging
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from certifier.models import TrackerCertification


logger = logging.getLogger(__name__)


def render_component(component, component_lowstat):  # pragma: no cover
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


def render_generic_state(state: str = "", state_map: dict = {}):  # pragma: no cover
    """
    Renders an HTML div using the state as the key to the state map dict,
    containing the classes that should be applied to the div for the state
    """
    if not state in state_map:
        return state
    return mark_safe(f'<div class="{state_map[state]}">{state}</div>')


def render_certify_button(run_number, dataset_express, dataset_prompt, dataset_rereco):
    """
    Deprecated!

    Button that redirects to certifying the next available dataset
    for a given run number.
    """
    css_class = None

    if (
        TrackerCertification.objects.filter(
            runreconstruction__run__run_number=run_number,
            runreconstruction__reconstruction="express",
        ).exists()
        and TrackerCertification.objects.filter(
            runreconstruction__run__run_number=run_number,
            runreconstruction__reconstruction="prompt",
        ).exists()
        and TrackerCertification.objects.filter(
            runreconstruction__run__run_number=run_number,
            runreconstruction__reconstruction="rereco",
        ).exists()
        and TrackerCertification.objects.filter(
            runreconstruction__run__run_number=run_number,
            runreconstruction__reconstruction="rerecoul",
        ).exists()
    ):
        return mark_safe(
            '<div align="center">'
            '<button class="btn btn-block btn-info" disabled id="id_table_certify">{}</button>'
            "</div>".format("Certified")
        )
    else:
        return mark_safe(
            '<div align="center">'
            '<a href="{}">'
            '<button class="btn btn-block btn-info" id="id_table_certify">'
            "Certify This Run"
            "</button>"
            "</a>"
            "</div>".format(reverse("certify", kwargs={"run_number": run_number}))
        )


def render_dataset(run_number, dataset, state, reco, user):  # pragma: no cover
    """
    Function that renders the per-dataset button on the OpenRunsTable.
    """
    try:
        certification = TrackerCertification.objects.get(
            runreconstruction__run__run_number=run_number,
            runreconstruction__reconstruction=reco,
        )
        exists = True
    except TrackerCertification.DoesNotExist:
        exists = False

    # If already exists or not Open, allow user to update the entry
    if state != "OPEN" or exists:
        if exists and certification.user == user:
            return mark_safe(
                '<div align="center">'
                '<a href="{0}">'
                '<button class="btn btn-block btn-success" id="id_table_certify" title="Update existing certification">'
                "{1}"
                "</button>"
                "</a>"
                "</div>".format(
                    reverse(
                        "listruns:update",
                        kwargs={
                            "pk": TrackerCertification.objects.get(
                                runreconstruction__run__run_number=run_number,
                                runreconstruction__reconstruction=reco,
                            ).pk,
                            "run_number": run_number,
                            "reco": reco,
                        },
                    ),
                    dataset,
                )
            )
        # State is NOT open AND (Certification does not exist OR user is same with request)
        return mark_safe(
            '<div align="center">'
            '<button class="btn btn-block btn-success" id="id_table_certify" disabled title="Booked by another user!">'
            '<font color="black">{}</font>'
            "</button>"
            "</div>".format(dataset)
        )
    # Reconstruction state is OPEN and There's no certification yet
    return mark_safe(
        '<div align="center">'
        '<a href="{0}?dataset={1}">'
        '<button class="btn btn-block btn-warning" id="id_table_certify" title="Available for certification">'
        "{1}"
        "</button>"
        "</a>"
        "</div>".format(reverse("certify", kwargs={"run_number": run_number}), dataset)
    )


def render_trackermap(trackermap):  # pragma: no cover
    if trackermap == "Missing":
        return mark_safe('<div class="bad-component">{}</div>'.format(trackermap))
    return trackermap


def render_boolean_cell(value):  # pragma: no cover
    boolean_value = False if value is False or value == "0" or value == 0 else True
    logger.debug(f"{value} {boolean_value}")
    glyphicon = "ok" if boolean_value else "remove"

    html = '<span class="glyphicon glyphicon-{}"></span>'.format(glyphicon, glyphicon)

    return mark_safe(html)
