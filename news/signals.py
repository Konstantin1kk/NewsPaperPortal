from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory


@receiver(signal=m2m_changed, sender=PostCategory)
def post_created(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        # список категорий у созданного поста
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        token_post = None
        if instance.post_type == 'AR':
            token_post = 'articles'
        else:
            token_post = 'news'

        subject = f'Новый пост в категории {instance.category}'

        text_content = (
            f'Ссылка на пост: http://127.0.0.1:8000/posts/{token_post}/{instance.pk}'
            f'Пост {instance.post_type}'
            f'Автор {instance.author}'
            f'{instance.preview()}'
        )

        html_content = (
            f'<a href=http://127.0.0.1:8000/posts/{token_post}/{instance.pk}>Ссылка на пост</a><br><br>'
            f'Пост {instance.post_type}<br>'
            f'Автор {instance.author}<br>'
            f'{instance.preview()}'
        )

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=None, to=[subscriber.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
    else:
        return
