from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import SignUpUserForm


class SignUpUserView(CreateView):
    model = User
    form_class = SignUpUserForm
    success_url = 'accounts/login'
    template_name = 'registration/login.html'
