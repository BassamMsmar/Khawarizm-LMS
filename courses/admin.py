from django.contrib import admin
from .models import Course, Lesson

class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('name', 'lecturer', 'is_active')
    search_fields = ('name', 'lecturer__full_name')
    ordering = ('name',)
admin.site.register(Course, CourseAdmin)


class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('title', 'course', 'lesson_type', 'is_active')
    list_filter = ('course', 'lesson_type', 'is_active')
    search_fields = ('title', 'course__name', 'lesson_type')
    ordering = ('title',)
admin.site.register(Lesson, LessonAdmin)

# Register your models here.
