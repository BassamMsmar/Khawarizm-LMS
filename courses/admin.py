from django.contrib import admin
from .models import Course, Lesson, Quiz, Question, Unit, Choice

class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('title', 'lecturer', 'is_active')
    search_fields = ('title', 'lecturer__full_name')
    ordering = ('title',)
admin.site.register(Course, CourseAdmin)

admin.site.register(Unit)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)

class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('title', 'course', 'lesson_type', 'is_active')
    list_filter = ('course', 'lesson_type', 'is_active')
    search_fields = ('title', 'course__title', 'lesson_type')
    ordering = ('title',)
admin.site.register(Lesson, LessonAdmin)

# Register your models here.
