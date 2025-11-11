from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Lesson, Subscription
from .validators import YouTubeURLValidator

User = get_user_model()


class YouTubeURLValidatorTestCase(TestCase):
    """Тесты для валидатора YouTube ссылок."""

    def setUp(self) -> None:
        self.validator = YouTubeURLValidator()

    def test_validator_has_required_attributes(self) -> None:
        """Тест наличия обязательных атрибутов у валидатора."""
        self.assertTrue(hasattr(self.validator, "__fields__"))
        self.assertEqual(self.validator.__fields__, ["video_url"])
        self.assertTrue(callable(self.validator))

    def test_valid_youtube_urls(self) -> None:
        """Тест валидных YouTube ссылок."""
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ]

        for url in valid_urls:
            with self.subTest(url=url):
                try:
                    self.validator(url)
                except ValidationError:
                    self.fail(f"Validator raised ValidationError for valid URL: {url}")

    def test_invalid_youtube_urls(self) -> None:
        """Тест невалидных YouTube ссылок."""
        invalid_urls = [
            "https://vk.com/video/test",
            "https://rutube.ru/video/test",
            "https://example.com/video",
            "https://vimeo.com/123456",
        ]

        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValidationError):
                    self.validator(url)

    def test_empty_url(self) -> None:
        """Тест пустой ссылки."""
        try:
            self.validator("")
            self.validator(None)
        except ValidationError:
            self.fail("Validator raised ValidationError for empty URL")


class CourseModelTestCase(TestCase):
    """Тесты модели Course."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@user.com", password="testpass123"
        )

    def test_course_creation(self) -> None:
        """Тест создания курса."""
        course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )
        self.assertEqual(course.title, "Test Course")
        self.assertEqual(course.owner, self.user)
        self.assertEqual(str(course), "Test Course")

    def test_course_ordering(self) -> None:
        """Тест ordering в мета классе курса."""
        course1 = Course.objects.create(title="Course 1", owner=self.user)
        course2 = Course.objects.create(title="Course 2", owner=self.user)
        courses = Course.objects.all()
        self.assertEqual(courses[0], course2)
        self.assertEqual(courses[1], course1)


class LessonModelTestCase(TestCase):
    """Тесты модели Lesson."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@user.com", password="testpass123"
        )
        self.course = Course.objects.create(title="Test Course", owner=self.user)

    def test_lesson_creation(self) -> None:
        """Тест создания урока."""
        lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_url="https://www.youtube.com/watch?v=test",
        )
        self.assertEqual(lesson.title, "Test Lesson")
        self.assertEqual(lesson.course, self.course)
        self.assertEqual(lesson.owner, self.user)
        expected_str = f"{lesson.title} ({self.course.title})"
        self.assertEqual(str(lesson), expected_str)

    def test_lesson_ordering(self) -> None:
        """Тест ordering в мета классе урока."""
        lesson1 = Lesson.objects.create(
            title="Lesson 1", course=self.course, owner=self.user
        )
        lesson2 = Lesson.objects.create(
            title="Lesson 2", course=self.course, owner=self.user
        )
        lessons = Lesson.objects.all()
        self.assertEqual(lessons[0], lesson1)
        self.assertEqual(lessons[1], lesson2)

    def test_lesson_video_url_validation(self) -> None:
        """Тест валидации видео URL."""
        lesson = Lesson(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_url="https://vk.com/video/invalid",
        )
        with self.assertRaises(ValidationError):
            lesson.full_clean()


class SubscriptionModelTestCase(TestCase):
    """Тесты модели Subscription."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@user.com", password="testpass123"
        )
        self.course = Course.objects.create(title="Test Course", owner=self.user)

    def test_subscription_creation(self) -> None:
        """Тест создания подписки."""
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        expected_str = f"{self.user.email} - {self.course.title}"
        self.assertEqual(str(subscription), expected_str)

    def test_subscription_unique_together(self) -> None:
        """Тест уникальности подписки user+course."""
        Subscription.objects.create(user=self.user, course=self.course)
        with self.assertRaises(Exception):
            Subscription.objects.create(user=self.user, course=self.course)


class LessonCRUDTestCase(TestCase):
    """Тесты CRUD операций для уроков."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@user.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            email="admin@user.com", password="adminpass123", is_staff=True
        )
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )
        self.lesson_data = {
            "title": "Test Lesson",
            "description": "Test Lesson Description",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=test",
        }

    def test_lesson_create_authenticated(self) -> None:
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/materials/lessons/create/", self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().title, "Test Lesson")

    def test_lesson_create_unauthenticated(self) -> None:
        response = self.client.post("/api/materials/lessons/create/", self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list_authenticated(self) -> None:
        Lesson.objects.create(title="Test Lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/materials/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_lesson_retrieve_owner(self) -> None:
        lesson = Lesson.objects.create(
            title="Test Lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/materials/lessons/{lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")

    def test_lesson_update_owner(self) -> None:
        lesson = Lesson.objects.create(
            title="Test Lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        update_data = {"title": "Updated Lesson"}
        response = self.client.patch(
            f"/api/materials/lessons/{lesson.id}/update/", update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, "Updated Lesson")

    def test_lesson_delete_owner(self) -> None:
        lesson = Lesson.objects.create(
            title="Test Lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/materials/lessons/{lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_admin(self) -> None:
        lesson = Lesson.objects.create(
            title="Test Lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/materials/lessons/{lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(TestCase):
    """Тесты функционала подписок на курсы."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@user.com", password="testpass123"
        )
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

    def test_subscription_create(self) -> None:
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/materials/subscription/", {"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_delete(self) -> None:
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/materials/subscription/", {"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_unauthenticated(self) -> None:
        response = self.client.post(
            "/api/materials/subscription/", {"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ValidatorStructureTestCase(TestCase):
    """Тесты структуры валидатора."""

    def test_validator_has_call_method(self) -> None:
        """Тест что валидатор имеет метод __call__."""
        validator = YouTubeURLValidator()
        self.assertTrue(hasattr(validator, "__call__"))
        self.assertTrue(callable(validator))

    def test_validator_has_fields_property(self) -> None:
        """Тест что валидатор имеет свойство __fields__."""
        validator = YouTubeURLValidator()
        self.assertTrue(hasattr(validator, "__fields__"))
        self.assertEqual(validator.__fields__, ["video_url"])
        self.assertIsInstance(validator.__fields__, list)
        