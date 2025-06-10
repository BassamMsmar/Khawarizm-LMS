from django.contrib import admin
from .models import Language, StudentProfile, LecturerProfile


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'department', 'created_at')
    list_filter = ('college', 'department', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('course', 'languages',)
    autocomplete_fields = ['college', 'department']
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'created_at')
    list_filter = ('experience', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('colleges', 'departments', 'course', 'languages')
    readonly_fields = ('created_at', 'updated_at')
