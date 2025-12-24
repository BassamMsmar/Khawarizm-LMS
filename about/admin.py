from django.contrib import admin
from .models import AboutPage

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'sub_title', 'description', 'content')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

