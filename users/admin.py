from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from .models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'city')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_method', 'payment_date', 'paid_course', 'paid_lesson')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('user__email', 'paid_course__title', 'paid_lesson__title')
    raw_id_fields = ('user', 'paid_course', 'paid_lesson')


admin.site.unregister(Group)


@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    """
    Кастомная админка для групп с дополнительной информацией
    """
    list_display = ('name', 'get_user_count', 'get_permissions_count')
    list_filter = ('name',)
    search_fields = ('name',)

    def get_user_count(self, obj):
        """Количество пользователей в группе"""
        return obj.user_set.count()
    get_user_count.short_description = 'Количество пользователей'

    def get_permissions_count(self, obj):
        """Количество разрешений в группе"""
        return obj.permissions.count()
    get_permissions_count.short_description = 'Количество разрешений'
