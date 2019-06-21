import django_filters
from django import forms
from users.models import User
from oms.models import OmsRun, OmsFill
from django.db import models
from django.forms.widgets import SelectDateWidget
from django.utils import timezone

from certifier.models import TrackerCertification, Dataset, PixelProblem

class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass

class ShiftLeaderTrackerCertificationFilter(django_filters.FilterSet):
    # user = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all())
    user = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='user',
        to_field_name='pk',
        queryset=User.objects.all().order_by("first_name", "last_name", "username"),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '10',
        })
    )

    runreconstruction__run__b_field = django_filters.ModelChoiceFilter(queryset=OmsRun.objects.values_list("b_field", flat=True).distinct(),
                                            widget=forms.Select(attrs={
                                                'class': 'form-control',
                                            }))

    runreconstruction__run__fill__fill_type_runtime = django_filters.ModelChoiceFilter(queryset=OmsFill.objects.values_list("fill_type_runtime", flat=True).distinct(),
                                            widget=forms.Select(attrs={
                                                'class': 'form-control',
                                            }))

    runreconstruction__run__energy = django_filters.ModelChoiceFilter(queryset=OmsRun.objects.values_list("energy", flat=True).distinct(),
                                            widget=forms.Select(attrs={
                                                'class': 'form-control',
                                            }))

    runreconstruction__run__run_type = django_filters.ModelChoiceFilter(queryset=OmsRun.objects.values_list("run_type", flat=True).distinct(),
                                            widget=forms.Select(attrs={
                                                'class': 'form-control',
                                            }))

    runreconstruction__run__run_number__in = InFilter(field_name='runreconstruction__run__run_number', lookup_expr='in')

    date__gte = django_filters.DateFilter(
        'date',
        label='Date greater than',
        lookup_expr='gte',
        widget=forms.SelectDateWidget(
            years=range(2018, timezone.now().year + 1),
            attrs={'class': 'form-control'},
        ),
    )

    dataset = django_filters.ModelChoiceFilter(
        queryset=Dataset.objects.all(),
        widget=forms.Select()
    )

    date__lte = django_filters.DateFilter(
        'date',
        label='Date less than',
        lookup_expr='lte',
        widget=forms.SelectDateWidget(
            years=range(2018, timezone.now().year + 1),
            attrs={'class': 'form-control'},
        ),
    )

    class Meta:
        model = TrackerCertification
        fields = {
            'date': ['gte', 'lte', ],
            'runreconstruction__run__run_number': ['gte', 'lte', ],
            'runreconstruction__reconstruction': ['exact'],
            'pixel_problems': ['exact'],
            'strip_problems': ['exact'],
            'tracking_problems': ['exact'],
        }
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f: {
                    'widget': SelectDateWidget
                },
            },
        }
