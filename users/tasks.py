from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def deactivate_inactive_users():
    """
    Задача для блокировки пользователей, которые не заходили более месяца.
    """
    try:
        one_month_ago = timezone.now() - timedelta(days=30)

        inactive_users = User.objects.filter(
            last_login__lt=one_month_ago, is_active=True
        )

        count = inactive_users.count()
        inactive_users.update(is_active=False)

        return f"Заблокировано {count} неактивных пользователей"

    except Exception as e:
        return f"Ошибка при блокировке пользователей: {str(e)}"
