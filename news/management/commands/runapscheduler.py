import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post

logger = logging.getLogger(__name__)


def my_job():
    posts = Post.objects.order_by('rating')[:3]
    text = '/n'.join(['{} - {}'.format(post.title, post.rating) for post in posts])
    mail_managers('Посты с низкой оценкой: ', text)


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
            trigger=CronTrigger(minute='20', hour='10'),
            id='my_job',
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'my_job'.")

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
