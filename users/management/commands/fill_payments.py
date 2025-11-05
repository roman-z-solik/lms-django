from django.core.management.base import BaseCommand
from users.models import User, Payment
from materials.models import Course, Lesson
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми платежами'

    def handle(self, *args, **options):
        user1, created = User.objects.get_or_create(
            email='testuser1@example.com',
            defaults={
                'first_name': 'Иван',
                'last_name': 'Петров',
                'is_staff': False,
                'is_superuser': False
            }
        )
        user1.set_password('12345')
        user1.save()

        user2, created = User.objects.get_or_create(
            email='testuser2@example.com',
            defaults={
                'first_name': 'Мария',
                'last_name': 'Сидорова',
                'is_staff': False,
                'is_superuser': False
            }
        )
        user2.set_password('12345')
        user2.save()

        course1, created = Course.objects.get_or_create(
            title='Python для начинающих',
            defaults={'description': 'Базовый курс по Python'}
        )

        course2, created = Course.objects.get_or_create(
            title='Django Framework',
            defaults={'description': 'Веб-разработка на Django'}
        )

        lesson1, created = Lesson.objects.get_or_create(
            course=course1,
            title='Введение в Python',
            defaults={
                'description': 'Основы языка Python',
                'video_url': 'https://youtube.com/watch?v=python_intro'
            }
        )

        lesson2, created = Lesson.objects.get_or_create(
            course=course2,
            title='Модели в Django',
            defaults={
                'description': 'Работа с моделями Django',
                'video_url': 'https://youtube.com/watch?v=django_models'
            }
        )

        payments_data = [
            {
                'user': user1,
                'paid_course': course1,
                'paid_lesson': None,
                'amount': Decimal('15000.00'),
                'payment_method': Payment.PAYMENT_METHOD_TRANSFER
            },
            {
                'user': user2,
                'paid_course': course2,
                'paid_lesson': None,
                'amount': Decimal('20000.00'),
                'payment_method': Payment.PAYMENT_METHOD_CASH
            },
            {
                'user': user1,
                'paid_course': None,
                'paid_lesson': lesson1,
                'amount': Decimal('2000.00'),
                'payment_method': Payment.PAYMENT_METHOD_TRANSFER
            },
            {
                'user': user2,
                'paid_course': None,
                'paid_lesson': lesson2,
                'amount': Decimal('2500.00'),
                'payment_method': Payment.PAYMENT_METHOD_CASH
            },
            {
                'user': user1,
                'paid_course': course2,
                'paid_lesson': None,
                'amount': Decimal('18000.00'),
                'payment_method': Payment.PAYMENT_METHOD_TRANSFER
            },
        ]

        created_count = 0
        for payment_data in payments_data:
            payment, created = Payment.objects.get_or_create(
                user=payment_data['user'],
                paid_course=payment_data['paid_course'],
                paid_lesson=payment_data['paid_lesson'],
                defaults={
                    'amount': payment_data['amount'],
                    'payment_method': payment_data['payment_method']
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {created_count} платежей. Всего платежей в базе: {Payment.objects.count()}'
            )
        )
