from rest_framework import viewsets, permissions, generics
from drf_yasg.utils import swagger_auto_schema
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.

    Предоставляет следующие действия:
    - list: Получить список всех курсов
    - create: Создать новый курс
    - retrieve: Получить детальную информацию о курсе
    - update: Полностью обновить курс
    - partial_update: Частично обновить курс
    - destroy: Удалить курс
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class LessonListView(generics.ListAPIView):
    """
    Generic-класс для получения списка всех уроков.

    Возвращает пагинированный список всех уроков в системе.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonRetrieveView(generics.RetrieveAPIView):
    """
    Generic-класс для получения детальной информации об уроке.

    Возвращает полную информацию об указанном уроке.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonCreateView(generics.CreateAPIView):
    """
    Generic-класс для создания нового урока.

    Позволяет создать новый урок с указанием курса, названия, описания и других данных.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonUpdateView(generics.UpdateAPIView):
    """
    Generic-класс для обновления существующего урока.

    Позволяет обновить информацию об уроке. Поддерживает частичное обновление (PATCH).
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonDestroyView(generics.DestroyAPIView):
    """
    Generic-класс для удаления урока.

    Полностью удаляет указанный урок из системы.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]
