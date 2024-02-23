from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category


class PostForm(forms.ModelForm):
    post_type_choices = [
        ('NW', 'Новость'),
        ('AR', 'Статья'),
    ]
    post_type = forms.ChoiceField(
        choices=post_type_choices,
        label='Post type',
        widget=forms.Select()
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Category',
        widget=forms.Select()
    )
    title = forms.CharField(
        label='Title',
        widget=forms.CharField()
    )
    text = forms.TextInput()
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'category', 'title', 'text']
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data['title']
        text = cleaned_data['text']
        if title or text is None:
            raise ValidationError(
                'Поле/поля не могут быть пустыми.'
            )
        