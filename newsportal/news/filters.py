"""
filters to facilitate search
"""
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from django.forms import DateInput
from .models import Category


class PostFilter(FilterSet):
    header = CharFilter(
        field_name='header',
        lookup_expr='icontains',
        label='Title'
    )
    category = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Any'
    )
    date_before = DateFilter(
        field_name='dateCreated',
        lookup_expr='lte',
        label='Published after',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        )
    )
    date_after = DateFilter(
        field_name='dateCreated',
        lookup_expr='gte',
        label='Published after',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        )
    )
