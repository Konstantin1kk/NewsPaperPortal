from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        articles_author = Post.objects.filter(author=self).aggregate(aa=Coalesce(Sum('rating'), 0))['aa']
        comments_author = Comment.objects.filter(user=self.user).aggregate(ca=Coalesce(Sum('rating'), 0))['ca']
        comments_to_author = Comment.objects.filter(post__author=self).aggregate(cta=Coalesce(Sum('rating'), 0))['cta']

        self.rating = articles_author * 3 + comments_author + comments_to_author
        self.save()
        
    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_type = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', through='Subscriptions')
    
    def __str__(self):
        return self.category_type


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    CHOICES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    date_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(choices=CHOICES, default=article, max_length=2)
    category = models.ManyToManyField(Category, through='PostCategory')

    title = models.CharField(max_length=120)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def get_absolute_url(self):
        post_type = None
        if self.post_type == 'NW':
            post_type = 'news'
        else:
            post_type = 'articles'

        return f'{post_type}/{self.pk}'

    def __str__(self):
        return f'{self.title}: rating {self.rating}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.CharField(max_length=150)
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriptions(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='subscriptions')
