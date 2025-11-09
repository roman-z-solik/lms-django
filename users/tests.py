from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Payment
from materials.models import Course, Lesson

User = get_user_model()


class UserManagerTestCase(TestCase):
    """Тесты кастомного менеджера пользователей."""

    def test_create_user_without_email(self) -> None:
        """Тест создания пользователя без email."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpass123")

    def test_create_superuser_is_staff_false(self) -> None:
        """Тест создания суперпользователя с is_staff=False."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com", password="testpass123", is_staff=False
            )

    def test_create_superuser_is_superuser_false(self) -> None:
        """Тест создания суперпользователя с is_superuser=False."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com", password="testpass123", is_superuser=False
            )


class UserModelTestCase(TestCase):
    """Тесты модели пользователя."""

    def test_create_user(self) -> None:
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), "test@example.com")

    def test_create_superuser(self) -> None:
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_optional_fields(self) -> None:
        """Тест необязательных полей пользователя."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            phone="+79999999999",
            city="Moscow",
        )
        self.assertEqual(user.phone, "+79999999999")
        self.assertEqual(user.city, "Moscow")


class PaymentModelTestCase(TestCase):
    """Тесты модели платежей."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_payment_creation_cash(self) -> None:
        """Тест создания платежа наличными."""
        payment = Payment.objects.create(
            user=self.user, amount=1000.00, payment_method=Payment.PAYMENT_METHOD_CASH
        )
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount, 1000.00)
        self.assertEqual(payment.payment_method, Payment.PAYMENT_METHOD_CASH)

    def test_payment_creation_transfer(self) -> None:
        """Тест создания платежа переводом."""
        payment = Payment.objects.create(
            user=self.user,
            amount=1500.00,
            payment_method=Payment.PAYMENT_METHOD_TRANSFER,
        )
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount, 1500.00)
        self.assertEqual(payment.payment_method, Payment.PAYMENT_METHOD_TRANSFER)

    def test_payment_str_representation(self) -> None:
        payment = Payment.objects.create(
            user=self.user, amount=1500.00, payment_method=Payment.PAYMENT_METHOD_CASH
        )
        expected_str = f"Платеж {self.user.email} - {1500.00} руб."
        self.assertEqual(str(payment), expected_str)

    def test_payment_ordering(self) -> None:
        """Тест ordering в мета классе платежей."""
        payment1 = Payment.objects.create(user=self.user, amount=1000.00)
        payment2 = Payment.objects.create(user=self.user, amount=2000.00)
        payments = Payment.objects.all()
        self.assertEqual(payments[0], payment2)
        self.assertEqual(payments[1], payment1)


class PaymentValidationTestCase(TestCase):
    """Тесты валидации платежей."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_payment_clean_method_both_course_and_lesson(self) -> None:
        course = Course.objects.create(title="Test Course", owner=self.user)
        lesson = Lesson.objects.create(
            title="Test Lesson", course=course, owner=self.user
        )

        payment = Payment(
            user=self.user, paid_course=course, paid_lesson=lesson, amount=1000.00
        )

        with self.assertRaises(ValidationError) as context:
            payment.clean()

        self.assertIn(
            "Нельзя оплатить одновременно и курс и урок", str(context.exception)
        )

    def test_payment_clean_method_neither_course_nor_lesson(self) -> None:
        payment = Payment(user=self.user, amount=1000.00)

        with self.assertRaises(ValidationError) as context:
            payment.clean()

        self.assertIn(
            "Необходимо указать либо курс, либо урок для оплаты", str(context.exception)
        )

    def test_payment_clean_method_valid_course_only(self) -> None:
        """Тест валидного платежа только с курсом."""
        course = Course.objects.create(title="Test Course", owner=self.user)

        payment = Payment(user=self.user, paid_course=course, amount=1000.00)

        try:
            payment.clean()
        except ValidationError:
            self.fail(
                "clean() raised ValidationError for valid payment with course only"
            )

    def test_payment_clean_method_valid_lesson_only(self) -> None:
        """Тест валидного платежа только с уроком."""
        course = Course.objects.create(title="Test Course", owner=self.user)
        lesson = Lesson.objects.create(
            title="Test Lesson", course=course, owner=self.user
        )

        payment = Payment(user=self.user, paid_lesson=lesson, amount=1000.00)

        try:
            payment.clean()
        except ValidationError:
            self.fail(
                "clean() raised ValidationError for valid payment with lesson only"
            )
