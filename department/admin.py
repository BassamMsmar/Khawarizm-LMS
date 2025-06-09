from django.contrib import admin
from .models import Department, DegreeLevel


class DepartmentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('name', 'college', 'degree_level', 'is_active')
    list_filter = ('college', 'degree_level', 'is_active')
    search_fields = ('name', 'college__name', 'degree_level__name')
    ordering = ('name',)
admin.site.register(Department, DepartmentAdmin)

class DegreeLevelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)
admin.site.register(DegreeLevel, DegreeLevelAdmin)

# Register your models here.
