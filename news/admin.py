from django.contrib import admin
from .models import Category, Post
from modeltranslation.admin import TranslationAdmin


@admin.register(Post)
class PostTranslateAdmin(TranslationAdmin):
    list_display = ('author', 'post_type', 'rating')
    list_filter = ('rating', 'date_time', 'post_type')
    search_fields = ('author', 'title')


@admin.register(Category)
class CategoryTranslateAdmin(TranslationAdmin):
    list_display = ('category_type', )
    list_filter = ('category_type', )
    search_fields = ('category_type', )
