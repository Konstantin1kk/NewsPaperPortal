from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from .models import Post, Category, Subscriptions
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.core.cache import cache


# all posts
class PostListView(ListView):
    model = Post
    ordering = 'date_time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10
    

class PostDetailView(DetailView):
    model = Post
    ordering = 'date_time'
    template_name = 'new.html'
    context_object_name = 'post'
    

class PostSearchView(ListView):
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


# posts: news
class NewsListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='NW')
    
    
class NewsDetailView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        self.queryset = super().get_queryset().filter(post_type='NW')
        return self.queryset

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if obj is None:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj
    

class NewsSearchView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(post_type='NW')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    

class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'create.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_post')
    raise_exception = True
    
    def get_queryset(self):
        return self.model.objects.filter(post_type='NW')
    
    def form_valid(self, form):
        form.instance.post_type = 'NW'
        return super().form_valid(form)
    

class NewsEditView(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'edit.html'
    permission_required = ('news.change_post')
    raise_exception = True
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='NW')
    
    def get_success_url(self):
        pk = self.get_object().pk
        return reverse_lazy('new', kwargs={'pk': pk})


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post')
    raise_exception = True
        
    def get_queryset(self):
        return super().get_queryset().filter(post_type='NW')


# posts: articles
class ArticleListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')
    
    
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')
    
    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))
    

class ArticleSearchView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(post_type='AR')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'create.html'
    success_url = reverse_lazy('articles_list')
    permission_required = ('news.add_post')
    raise_exception = True
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')
    
    def form_valid(self, form):
        form.instance.post_type = 'AR'
        return super().form_valid(form)
    

class ArticleEditView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'edit.html'
    permission_required = ('news.change_post')
    raise_exception = True
    
    def get_queryset(self):
        self.queryset = self.model.objects.filter(post_type='AR')
        return self.queryset
    
    def get_success_url(self):
        pk = self.get_object().pk
        return reverse_lazy('article', kwargs={'pk': pk})
    
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))
    
    
class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('articles_list')
    permission_required = ('news.delete_post')
    raise_exception = True
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        if action == 'subscribe':
            Subscriptions.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriptions.objects.get(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(
        Subscriptions.objects.filter(user=request.user, category=OuterRef('pk'))
        )
    ).order_by('category_type')

    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions})
