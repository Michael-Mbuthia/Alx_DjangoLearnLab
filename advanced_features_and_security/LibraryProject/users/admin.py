from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    Extends Django's default UserAdmin with additional fields.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = UserAdmin.list_filter + ('date_of_birth',)
    search_fields = UserAdmin.search_fields + ('email', 'first_name', 'last_name')
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
