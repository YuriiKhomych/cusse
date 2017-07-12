from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


class CustomUserAdmin(UserAdmin):
    search_fields = ("first_name", "last_name", "username", "email")
    add_fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'photo', 'birthday','country', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', )


admin.site.register(User, CustomUserAdmin)
