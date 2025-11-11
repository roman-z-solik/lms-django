from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "phone", "city", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "city")
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {"fields": ("first_name", "last_name", "phone", "city", "avatar")},
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone",
                    "city",
                ),
            },
        ),
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


admin.site.unregister(Group)


@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    """
    Кастомная админка для групп с дополнительной информацией
    """

    list_display = ("name", "get_user_count", "get_permissions_count")
    list_filter = ("name",)
    search_fields = ("name",)

    def get_user_count(self, obj):
        """Количество пользователей в группе"""
        return obj.user_set.count()

    get_user_count.short_description = "Количество пользователей"

    def get_permissions_count(self, obj):
        """Количество разрешений в группе"""
        return obj.permissions.count()

    get_permissions_count.short_description = "Количество разрешений"
    