from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import post_create


@receiver(signal=m2m_changed, sender=PostCategory)
def post_created(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        post_create.delay(instance)
