from django import forms
from .models import Author, Post, Category


class NewsForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Category',
        widget=forms.CheckboxSelectMultiple()
    )
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    text = forms.CharField(
        label='Text',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']
            

class ArticleForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Category',
        widget=forms.CheckboxSelectMultiple()
    )
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    text = forms.CharField(
        label='Text',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']
        