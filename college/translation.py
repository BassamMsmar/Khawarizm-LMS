from modeltranslation.translator import register, TranslationOptions
from .models import College

@register(College)
class CollegeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')