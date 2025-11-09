from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    title = models.CharField(_('title'), max_length=255)
    preview = models.ImageField(_('preview'), upload_to='courses/previews/', blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name=_('course')
    )
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    preview = models.ImageField(_('preview'), upload_to='lessons/previews/', blank=True, null=True)
    video_url = models.URLField(_('video URL'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title} ({self.course.title})"
