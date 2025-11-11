from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Course(models.Model):
    """
    Модель курса.
    """

    title = models.CharField(_("title"), max_length=255)
    preview = models.ImageField(
        _("preview"), upload_to="courses/previews/", blank=True, null=True
    )
    description = models.TextField(_("description"), blank=True, null=True)
    price = models.DecimalField(
        _("цена"), max_digits=10, decimal_places=2, default=0.00
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("owner"),
        related_name="courses",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Модель урока.
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("course"),
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    preview = models.ImageField(
        _("preview"), upload_to="lessons/previews/", blank=True, null=True
    )
    video_url = models.URLField(_("video URL"), blank=True, null=True)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("owner"),
        related_name="lessons",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Payment(models.Model):
    """
    Модель платежа для оплаты курсов через Stripe.
    """

    class Status(models.TextChoices):
        """Статусы платежа."""

        PENDING = "pending", _("Ожидает оплаты")
        PROCESSING = "processing", _("Обрабатывается")
        SUCCEEDED = "succeeded", _("Оплачен")
        FAILED = "failed", _("Ошибка оплаты")
        CANCELED = "canceled", _("Отменен")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("пользователь"),
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("курс"),
    )
    amount = models.DecimalField(_("сумма оплаты"), max_digits=10, decimal_places=2)
    stripe_product_id = models.CharField(
        _("ID продукта в Stripe"), max_length=255, blank=True, null=True
    )
    stripe_price_id = models.CharField(
        _("ID цены в Stripe"), max_length=255, blank=True, null=True
    )
    stripe_session_id = models.CharField(
        _("ID сессии в Stripe"), max_length=255, blank=True, null=True
    )
    payment_url = models.URLField(
        _("ссылка для оплаты"), max_length=500, blank=True, null=True
    )
    status = models.CharField(
        _("статус оплаты"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(_("создан"), auto_now_add=True)
    updated_at = models.DateTimeField(_("обновлен"), auto_now=True)

    class Meta:
        verbose_name = _("платеж")
        verbose_name_plural = _("платежи")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Платеж {self.id} - {self.user.email} - {self.amount}"


class Subscription(models.Model):
    """
    Модель подписки на обновления курса.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("пользователь"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("курс"),
    )
    subscribed_at = models.DateTimeField(_("дата подписки"), auto_now_add=True)
    is_active = models.BooleanField(_("активна"), default=True)

    class Meta:
        verbose_name = _("подписка")
        verbose_name_plural = _("подписки")
        unique_together = ["user", "course"]

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
