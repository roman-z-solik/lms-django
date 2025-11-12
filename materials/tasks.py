from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Course


@shared_task
def send_course_update_notification(course_id):
    """
    Задача для отправки уведомлений об обновлении курса подписанным пользователям.
    """
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(
            course=course, is_active=True
        ).select_related("user")

        for subscription in subscriptions:
            send_mail(
                subject=f'Курс "{course.title}" обновлен',
                message=f'Добрый день!\n\nКурс "{course.title}" был обновлен. Проверьте новые '
                f"материалы!\n\nС уважением,\nКоманда образовательной платформы",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )

        return (
            f"Отправлено уведомлений {subscriptions.count()} пользователям "
            f"для курса {course.title}"
        )

    except Course.DoesNotExist:
        return f"Курс с id {course_id} не найден"
    except Exception as e:
        return f"Ошибка отправки уведомлений: {str(e)}"


@shared_task
def send_lesson_update_notification(lesson_id, course_id):
    """
    Задача для отправки уведомлений об обновлении урока (с проверкой времени).
    """
    try:
        course = Course.objects.get(id=course_id)

        # Проверяем, что курс не обновлялся более 4 часов
        four_hours_ago = timezone.now() - timedelta(hours=4)
        if course.updated_at > four_hours_ago:
            return "Курс обновлялся недавно, уведомление не отправлено"

        subscriptions = Subscription.objects.filter(
            course=course, is_active=True
        ).select_related("user")

        for subscription in subscriptions:
            send_mail(
                subject=f'Урок в курсе "{course.title}" обновлен',
                message=f'Добрый день!\n\nВ курсе "{course.title}" был обновлен урок. Проверьте'
                f" новые материалы!\n\nС уважением,\nКоманда образовательной платформы",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )

        return f"Отправлено уведомлений об обновлении урока {subscriptions.count()} пользователям"

    except Exception as e:
        return f"Ошибка отправки уведомлений об уроке: {str(e)}"
