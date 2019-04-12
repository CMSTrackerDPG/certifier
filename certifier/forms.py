from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import TrackerCertification, BadReason, PixelProblem, StripProblem, TrackingProblem
from django.forms import ModelForm, RadioSelect, CheckboxSelectMultiple, ModelMultipleChoiceField
from checklists.forms import ChecklistFormMixin

class CertifyForm(ModelForm):

    pixel = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())
    strip = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())
    tracking = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())

    date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2017, timezone.now().year + 2)),
        initial=timezone.now
    )

    class Meta:
        model = TrackerCertification
        fields = [
            'pixel',
            'strip',
            'tracking',
            'pixel_lowstat',
            'strip_lowstat',
            'tracking_lowstat',
            'pixel_problems',
            'strip_problems',
            'tracking_problems',
            'bad_reason',
            'comment',
            'reference_runreconstruction',
            'date',
            'trackermap',
        ]

class CertifyFormWithChecklistForm(CertifyForm, ChecklistFormMixin):
    pass