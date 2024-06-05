from modeltranslation.translator import register, TranslationOptions
from .models import Post, Category


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    model = Category
    fields = ('category_type', )


@register(Post)
class PostTranslationOption(TranslationOptions):
    model = Post
    fields = ('title', 'text', )
