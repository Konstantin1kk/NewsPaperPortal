from django.db.models.query import QuerySet
from django.views.generic import (ListView, DetailView, CreateView)
from django.shortcuts import render
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsListView(ListView):
    model = Post
    ordering = 'date_time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10
    

class NewsDetailView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
    

class NewsListSearch(ListView):
    model = Post
    ordering = 'date_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    

class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create.html'
    

def index(request):
    return render(request, 'main.html')
