from .models import Post, Category
from modeltranslation.translator import translator, TranslationOptions


class PostTranslationOption(TranslationOptions):
    fields = ('title', 'text', )


class CategoryTranslationOption(TranslationOptions):
    fields = ('category_type', )


translator.register(Post, PostTranslationOption)
translator.register(Category, CategoryTranslationOption)
