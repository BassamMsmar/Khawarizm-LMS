from django.contrib import admin
from .models import DegreeLevel

class DegreeLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'college', 'department', 'courses',  'is_active', )
    list_filter = ('name', 'user', 'college', 'department', 'courses', 'is_active', )
    search_fields = ('name', 'user', 'college', 'department', 'courses', 'is_active', )
    ordering = ('name', 'user', 'college', 'department', 'courses', 'is_active', )

admin.site.register(DegreeLevel, DegreeLevelAdmin)

# Register your models here.
