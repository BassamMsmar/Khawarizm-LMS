from django.contrib import admin
from .models import College


class CollegeAdmin(admin.ModelAdmin):

    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'created_at', 'updated_at')
    ordering = ('name', 'description', 'created_at', 'updated_at')

admin.site.register(College, CollegeAdmin)
# Register your models here.
