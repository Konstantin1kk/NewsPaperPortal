import django_filters as filters
import django.forms as forms
from .models import Post, Category


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title',
    )
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label="All Categories",
        label='Categories',
        widget=forms.Select()
    )
    date_time = filters.DateTimeFilter(
        field_name='date_time',
        lookup_expr='gt',
        label='Date',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        )
    )
    
    class Meta:
        model = Post
        fields = ['title', 'category', 'date_time']
