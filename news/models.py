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


class Category(models.Model):
    category_type = models.CharField(max_length=100, unique=True)


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

    title = models.CharField(max_length=255)
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
