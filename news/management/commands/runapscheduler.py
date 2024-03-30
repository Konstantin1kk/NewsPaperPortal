import logging
import datetime
from django.template.loader import render_to_string
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from NewsPaperProject1 import settings

logger = logging.getLogger(__name__)


def my_job():
    posts = Post.objects.order_by('rating')[:3]
    text = '\n'.join(['{} - {}'.format(post.title, post.rating) for post in posts])
    mail_managers('Посты с низкой оценкой: ', text)

    categories = []
    for post in posts:
        categories += post.category.all()
    mails_users = User.objects.filter(subscriptions__category__in=categories).distinct().values_list('email', flat=True)

    subject = f'Возможно, эти посты вы еще не видели'
    text_content = (
        '\n'.join(['Ссылка на пост: http://127.0.0.1:8000/posts/{}'.format(post.get_absolute_url()) for post in posts])
    )

    html_content = (
        '\n'.join(['<a href=http://127.0.0.1:8000/posts/{}>Ссылка на пост</a>'.format(post.get_absolute_url()) for post in posts])
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=mails_users
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def my_job2():
    today = datetime.datetime.today()
    last_week = today - datetime.timedelta(days=7)
    past_posts = Post.objects.filter(date_time__gte=last_week)
    past_categories = past_posts.values_list('category', flat=True)
    subscribers = User.objects.filter(subscriptions__category__in=past_categories).values_list('email', flat=True)

    subject = 'Сводка новостей за неделю'
    html = render_to_string(
        template_name='weekly_newsletter.html',
        context={
            'posts': past_posts
        }
    )

    msg = EmailMultiAlternatives(subject=subject, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html, 'text/html')
    msg.send()


@util.close_old_connections
def delete_old_job_execution(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute='00', hour='13'),
            id='my_job',
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            my_job2,
            trigger=CronTrigger(minute='00', hour='18', day_of_week='FRI'),
            id='my_job2',
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'my_job2'.")

        scheduler.add_job(
            delete_old_job_execution,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')
