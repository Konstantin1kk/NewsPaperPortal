How to run the project:

1. clone this repository
2. download all libraries in requirements
3. download redis-server from github
4. use this commands:
   1. python manage.py runserver
   2. celery -A NewsPaperProject1 worker -l info
   3. celery -A NewsPaperProject1 beat -l INFO
