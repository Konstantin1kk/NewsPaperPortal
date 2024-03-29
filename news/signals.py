from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from NewsPaperProject1 import settings


@receiver(signal=m2m_changed, sender=PostCategory)
def post_created(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        users = User.objects.filter(subscriptions__category__in=categories).distinct()

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
