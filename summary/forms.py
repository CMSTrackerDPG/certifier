from django import forms
from summary.models import SummaryInfo


class SummaryExtraInfoForm(forms.ModelForm):
    class Meta:
        model = SummaryInfo
        fields = ["links_prompt_feedback", "special_comment"]
