from modeltranslation.translator import register, TranslationOptions
from .models import Post, Category


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('category_type', )


@register(Post)
class PostTranslationOption(TranslationOptions):
    fields = ('title', 'text', )
