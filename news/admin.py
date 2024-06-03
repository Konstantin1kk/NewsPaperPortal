from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Category, Post, Author
from modeltranslation.admin import TranslationAdmin


class PostAdmin(ModelAdmin):
    model = Post
    list_display = ('author', 'post_type', 'rating')
    list_filter = ('rating', 'date_time', 'post_type')
    search_fields = ('author', 'title')


@admin.register(Post)
class PostTranslateAdmin(TranslationAdmin, PostAdmin):
    model = Post


class CategoryAdmin(ModelAdmin):
    model = Category
    list_display = ('category_type',)
    list_filter = ('category_type',)
    search_fields = ('category_type',)


@admin.register(Category)
class CategoryTranslateAdmin(TranslationAdmin, CategoryAdmin):
    model = Category


admin.site.register(Author)
