from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpUserView.as_view(), name='signup'),
]
