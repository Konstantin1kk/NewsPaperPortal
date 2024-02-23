from django.urls import path
from .views import NewsListView, NewsDetailView, NewsListSearch, CreateView

urlpatterns = [
    path('', NewsListView.as_view()),
    path('<int:pk>/', NewsDetailView.as_view()),
    path('search/', NewsListSearch.as_view(), name='search'),
    path('create/', CreateView.as_view(), name='create'),
]
