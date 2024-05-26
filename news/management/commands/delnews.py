from django.core.management.base import BaseCommand
from news.models import Post


class Command(BaseCommand):
    help = 'Удаление новостей из категории'

    def add_arguments(self, parser):
        parser.add_argument('--category', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you really want to delete all news in this category? yes/no')

        answer = input('answer: ')

        if answer == 'yes':
            Post.objects.filter(category=options['--category']).delete()
            self.stdout.write(self.style.SUCCESS('Successfully wiped news'))

            return

        self.stdout.write(self.style.ERROR('Access denied'))
