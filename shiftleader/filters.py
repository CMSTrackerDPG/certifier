import django_filters
from django import forms
from users.models import User
from django.db import models
from django.forms.widgets import SelectDateWidget
from django.utils import timezone

from certifier.models import TrackerCertification, Dataset, PixelProblem

class ShiftLeaderTrackerCertificationFilter(django_filters.FilterSet):
    # user = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all())
    user = django_filters.filters.ModelMultipleChoiceFilter(
        name='user',
        to_field_name='pk',
        queryset=User.objects.all().order_by("first_name", "last_name", "username"),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '15',
        })
    )

    run_number__in = InFilter(field_name='runreconstruction__run__run_number', lookup_expr='in')

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
        }
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f: {
                    'widget': SelectDateWidget
                },
            },
        }
