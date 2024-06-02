from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('posts/', include('news.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]
