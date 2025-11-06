from django.contrib import admin
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("title", "description", "video_url", "preview", "owner", "course")
    readonly_fields = ("owner",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "owner")
    search_fields = ("title", "description", "owner__email")
    inlines = [LessonInline]
    readonly_fields = ("owner",)

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем владельца при создании"""
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "owner", "created_at", "updated_at")
    list_filter = ("course", "created_at", "updated_at", "owner")
    search_fields = ("title", "description", "course__title", "owner__email")
    raw_id_fields = ("course",)
    readonly_fields = ("owner",)

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем владельца при создании"""
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
