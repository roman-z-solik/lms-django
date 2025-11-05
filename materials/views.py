from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsModeratorOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Разграничение прав доступа для курсов:
        - Создание: только администраторы
        - Удаление: только администраторы
        - Просмотр и редактирование: администраторы и модераторы
        """
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]

        return [permission() for permission in permission_classes]


class LessonListView(generics.ListAPIView):
    """
    Generic-класс для получения списка уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]


class LessonRetrieveView(generics.RetrieveAPIView):
    """
    Generic-класс для получения одного урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]


class LessonCreateView(generics.CreateAPIView):
    """
    Generic-класс для создания урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]


class LessonUpdateView(generics.UpdateAPIView):
    """
    Generic-класс для изменения урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]


class LessonDestroyView(generics.DestroyAPIView):
    """
    Generic-класс для удаления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]
