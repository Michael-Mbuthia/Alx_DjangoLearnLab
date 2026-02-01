from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Book, CustomUser

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
    ordering = ('-id',)


admin.site.register(Book, BookAdmin)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = UserAdmin.list_filter + ('date_of_birth',)
    search_fields = UserAdmin.search_fields + ('email', 'first_name', 'last_name')
