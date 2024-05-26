from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'rating')
    list_filter = ('rating', 'date_time', 'post_type')
    search_fields = ('author', 'title')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
