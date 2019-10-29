from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import TrackerCertification, BadReason, PixelProblem, StripProblem, TrackingProblem, Dataset
from django.forms import ModelForm, RadioSelect, CheckboxSelectMultiple, ModelMultipleChoiceField, TextInput, Textarea
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
            'user',
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

class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ["dataset"]
        widgets = {
            'dataset': TextInput(
                attrs={'placeholder': "e.g. /Cosmics/Run2017F-PromptReco-v1/DQMIO",
                       'class': "form-control"}),
        }

class BadReasonForm(ModelForm):
    class Meta:
        model = BadReason
        fields = ["name", "description"]
        widgets = {
            'name': TextInput(
                attrs={'placeholder': "e.g. Timing Problem",
                        'class': "form-control",
                        'id':"id_bad_reason_name"}),
            'description': Textarea(
                attrs={'placeholder': "e.g. The problem consists in...",
                        'class': "form-control",
                        'rows' : "3",
                        'id':"id_bad_reason_desc"}),
        }

class CertifyFormWithChecklistForm(CertifyForm, ChecklistFormMixin):
    pass
