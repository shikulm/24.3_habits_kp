from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class UserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ('email', 'password')
        }),
        ('Профиль', {
            'classes': ['wide'],
            'fields': ('first_name', 'last_name', 'avatar')
        }),
        ('Разрешения', {
            'classes': ['wide'],
            'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')
        }),
        ('Дата', {
            'classes': ['wide'],
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    ordering = ("email",)


admin.site.register(
    User,
    UserAdmin
)
