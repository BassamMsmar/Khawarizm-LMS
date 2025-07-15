from django.contrib import admin
from .models import College, Question

class CollegeAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_students', 'difficulty_level', 'is_public', 'regular_price', 'discounted_price', 'tags', 'questions')
    list_filter = ('title', 'max_students', 'difficulty_level', 'is_public', 'regular_price', 'discounted_price', 'tags', 'questions')
    search_fields = ('title', 'max_students', 'difficulty_level', 'is_public', 'regular_price', 'discounted_price', 'tags', 'questions')
    ordering = ('title', 'max_students', 'difficulty_level', 'is_public', 'regular_price', 'discounted_price', 'tags', 'questions')

admin.site.register(College, CollegeAdmin)
admin.site.register(Question)
