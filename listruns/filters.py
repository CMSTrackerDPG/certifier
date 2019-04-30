import django_filters
from django import forms
from users.models import User
from django.db import models
from django.forms.widgets import SelectDateWidget
from django.utils import timezone

from certifier.models import TrackerCertification, Dataset, PixelProblem

class TrackerCertificationFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        'date',
        label='Date',
        lookup_expr='contains',
        widget=forms.SelectDateWidget(
            years=range(2018, timezone.now().year + 1),
            attrs={'class': 'form-control'},
        ),
    )

    date_range = django_filters.DateFromToRangeFilter(
        'date',
        widget=django_filters.widgets.RangeWidget(attrs={
            'placeholder': 'YYYY-MM-DD',
            'class': 'form-control',
            'size': 9,
            'maxlength': 10,
        })
    )

    runs = django_filters.RangeFilter(
        'runreconstruction__run__run_number',
        widget=django_filters.widgets.RangeWidget(attrs={
            'placeholder': 'run number',
            'class': 'form-control',
            'size': 7,
            'maxlength': 10,
        })
    )

    dataset = django_filters.ModelChoiceFilter(
        queryset=Dataset.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 500px;',
        })
    )

    class Meta:
        model = TrackerCertification
        fields = ['pixel_problems', 'strip_problems', 'tracking_problems']


class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass


class ShiftLeaderTrackerCertificationFilter(django_filters.FilterSet):
    # userid = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all())
    user = django_filters.filters.ModelMultipleChoiceFilter(
        name='user',
        to_field_name='pk',
        queryset=User.objects.all().order_by("first_name", "last_name", "username"),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '15',
        })
    )

    run_number__in = InFilter(field_name='runreconstruction', lookup_expr='in')

    date__gte = django_filters.DateFilter(
        'date',
        label='Date greater than',
        lookup_expr='gte',
        widget=forms.SelectDateWidget(
            years=range(2018, timezone.now().year + 1),
            attrs={'class': 'form-control'},
        ),
    )

    date__lte = django_filters.DateFilter(
        'date',
        label='Date lass than',
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
        }
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f: {
                    'widget': SelectDateWidget
                },
            },
        }


class ComputeLuminosityTrackerCertificationFilter(django_filters.FilterSet):
    class Meta:
        model = TrackerCertification
        fields = {
            'runreconstruction__run__run_number': ['gte', 'lte', ],
            'date': ['gte', 'lte', ],
        }


class RunsFilter(django_filters.FilterSet):
    runreconstruction__run__run_number__in = InFilter(field_name='runreconstruction', lookup_expr='in')

    class Meta:
        model = TrackerCertification
        fields = {
            'date': ['gte', 'lte', ],
            'runreconstruction__run__run_number': ['gte', 'lte', ],
            'reference_runreconstruction__run__run_number': ['gte', 'lte', ],
            'trackermap': ['exact'],
            'comment': ['exact'],
            'pixel': ['exact'],
            'strip': ['exact'],
            'tracking': ['exact'],
        }
