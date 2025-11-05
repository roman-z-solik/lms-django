from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner, IsOwnerOrModerator, IsNotModerator


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Разграничение прав доступа для курсов:
        - Создание: авторизованные пользователи (не модераторы)
        - Удаление: владелец или администратор
        - Просмотр и редактирование: владелец, модератор или администратор
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator | IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматически привязываем курс к текущему пользователю"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Фильтрация queryset:
        - Модераторы и администраторы видят все курсы
        - Обычные пользователи видят только свои курсы
        """
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()

        if user.is_staff or user.groups.filter(name='moderators').exists():
            return queryset

        return queryset.filter(owner=user)


class LessonListView(generics.ListAPIView):
    """
    Generic-класс для получения списка уроков.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator | IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Модераторы и администраторы видят все уроки
        - Обычные пользователи видят только свои уроки
        """
        user = self.request.user

        if user.is_staff or user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonRetrieveView(generics.RetrieveAPIView):
    """
    Generic-класс для получения одного урока.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator | IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Модераторы и администраторы видят все уроки
        - Обычные пользователи видят только свои уроки
        """
        user = self.request.user

        if user.is_staff or user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonCreateView(generics.CreateAPIView):
    """
    Generic-класс для создания урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        """Автоматически привязываем урок к текущему пользователю"""
        serializer.save(owner=self.request.user)


class LessonUpdateView(generics.UpdateAPIView):
    """
    Generic-класс для изменения урока.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator | IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Модераторы и администраторы могут редактировать все уроки
        - Обычные пользователи могут редактировать только свои уроки
        """
        user = self.request.user

        if user.is_staff or user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonDestroyView(generics.DestroyAPIView):
    """
    Generic-класс для удаления урока.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Администраторы могут удалять все уроки
        - Обычные пользователи могут удалять только свои уроки
        """
        user = self.request.user

        if user.is_staff:
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)
