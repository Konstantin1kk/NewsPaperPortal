from django.views.generic import ListView, DetailView
from .models import Post


class NewsListView(ListView):
    model = Post
    ordering = ['date_time']
    template_name = 'news.html'
    context_object_name = 'posts'


class NewsDetailView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
