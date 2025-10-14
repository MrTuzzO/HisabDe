from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    list_display = ['email', 'full_name', 'mobile', 'is_profile_complete', 'is_staff', 'is_active', 'created_at']
    list_filter = ['is_staff', 'is_active', 'is_profile_complete', 'created_at']
    search_fields = ['email', 'full_name', 'mobile']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'mobile')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Profile Status', {'fields': ('is_profile_complete',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('is_profile_complete', 'created_at', 'updated_at')
