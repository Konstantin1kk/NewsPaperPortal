from django.urls import path
from .views import NewsListView, NewsDetailView

urlpatterns = [
    path('', NewsListView.as_view()),
    path('<int:pk>/', NewsDetailView.as_view()),
]
