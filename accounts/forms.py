from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives, mail_managers


class SignUpUserForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Name')
    last_name = forms.CharField(label='Last name')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        

# for allauth
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        
        subject = 'Добро пожаловать в наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (f'<b>{user.username}</b>, вы успешно зарегистрировались на ' f'<a href="http://127.0.0.1:8000/posts/">сайте</a>!')
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        
        mail_managers(
            subject='Пользователь зарегистрировался',
            message=f'{user.username} зарегистрировался на сайте.'
        )
        return user
