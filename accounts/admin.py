from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'phone_number','profile_type','gender','date_of_birth', 'profile_picture', 'country', 'city', 'address', 'postal_code',
            'roles', 
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    readonly_fields = ('last_login', 'created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'display_roles', 'is_staff', 'is_superuser')
    list_display_links = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)
    filter_horizontal = ('roles',)  # لتسهيل اختيار الأدوار في الواجهة

    def display_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    display_roles.short_description = 'Roles'

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
