from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'description', 'video_url', 'preview')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'updated_at')
    list_filter = ('course', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'course__title')
    raw_id_fields = ('course',)


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
