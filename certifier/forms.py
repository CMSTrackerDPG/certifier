from django import forms
from django.core.exceptions import ValidationError

from .models import TrackerCertification, BadReason, PixelProblem, StripProblem, TrackingProblem
from django.forms import ModelForm, RadioSelect, CheckboxSelectMultiple, ModelMultipleChoiceField


class CertifyForm(ModelForm):

    pixel = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())
    strip = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())
    tracking = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())

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
        ]
