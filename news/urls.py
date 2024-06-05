from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(views.PostListView.as_view()), name='posts_list'),
    path('<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    
    path('news/', cache_page(60*5)(views.NewsListView.as_view()), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='new'),
    path('news/search/', views.NewsSearchView.as_view(), name='new_search'),
    path('news/create/', views.NewsCreateView.as_view(), name='new_create'),
    path('news/<int:pk>/edit/', views.NewsEditView.as_view(), name='new_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='new_delete'),
    
    path('articles/', views.ArticleListView.as_view(), name='articles_list'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article'),
    path('articles/search/', views.ArticleSearchView.as_view(), name='article_search'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleEditView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),

    path('subscriptions/', views.subscriptions, name='subscriptions'),
]
