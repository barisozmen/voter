import django_filters
from django import forms
from .models import Poll


class PollFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search polls...'})
    )
    
    tags = django_filters.CharFilter(
        field_name='tags__name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Filter by tag...'})
    )
    
    created_at = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )
    
    class Meta:
        model = Poll
        fields = ['title', 'tags', 'created_at', 'is_active']
