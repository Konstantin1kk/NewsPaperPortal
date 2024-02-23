from django.contrib import admin
from django.urls import path, include
from news import views


urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('articles/', include('news.urls')),
]
