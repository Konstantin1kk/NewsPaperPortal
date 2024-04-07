from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from .models import Post
from NewsPaperProject1 import settings
import datetime


@shared_task
def post_create(post_pk, *args, **kwargs):
    instance = Post.objects.get(pk=post_pk)
    category = instance.category.all()
    users = User.objects.filter(subscriptions__category__in=category).distinct()
    emails = [user.email for user in users]

    subject = f'Новый пост в категории/категориях: {[i for i in instance.category.all()]}'

    text = (
        f'Ссылка на пост: http://127.0.0.1:8000/posts/{instance.get_absolute_url()}'
        f'Пост: {instance.post_type}'
        f'Автор: {instance.author}'
        f'Краткое содержание: {instance.preview()}'
    )

    html = (
        f'--<a href=http://127.0.0.1:8000/posts/{instance.get_absolute_url()}>Ссылка на пост</a>--<br><br>'
        f'Пост: {instance.post_type}<br>'
        f'Автор: {instance.author}<br>'
        f'Краткое содержание: {instance.preview()}'
    )

    msg = EmailMultiAlternatives(subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=emails)
    msg.attach_alternative(html, 'text/html')
    msg.send()


@shared_task
def show_new_post(*args, **kwargs):
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_time__gte=last_week)
    categories_posts = posts.values_list('category', flat=True)
    subscribers = User.objects.filter(subscriptions__category__in=categories_posts).values_list('email', flat=True)

    subject = 'Сводка новостей за неделю'
    html = render_to_string(
        template_name='weekly_newsletter.html',
        context={
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(subject=subject, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html, 'text/html')
    msg.send()
