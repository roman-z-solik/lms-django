from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from materials.models import Course, Lesson


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=15, blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    avatar = models.ImageField(_('avatar'), upload_to='users/avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Payment(models.Model):
    """
    Модель платежей (Задание 2)
    """
    PAYMENT_METHOD_CASH = 'cash'
    PAYMENT_METHOD_TRANSFER = 'transfer'

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_CASH, 'Наличные'),
        (PAYMENT_METHOD_TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('пользователь')
    )
    payment_date = models.DateTimeField(
        _('дата оплаты'),
        auto_now_add=True
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name=_('оплаченный курс')
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name=_('оплаченный урок')
    )
    amount = models.DecimalField(
        _('сумма оплаты'),
        max_digits=10,
        decimal_places=2
    )
    payment_method = models.CharField(
        _('способ оплаты'),
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_TRANSFER
    )

    class Meta:
        verbose_name = _('платеж')
        verbose_name_plural = _('платежи')
        ordering = ['-payment_date']

    def __str__(self):
        return f"Платеж {self.user.email} - {self.amount} руб."

    def clean(self):
        """
        Валидация: нельзя оплатить и курс и урок одновременно
        """
        from django.core.exceptions import ValidationError
        if self.paid_course and self.paid_lesson:
            raise ValidationError('Нельзя оплатить одновременно и курс и урок. Выберите что-то одно.')
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError('Необходимо указать либо курс, либо урок для оплаты.')