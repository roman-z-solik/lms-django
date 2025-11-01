from rest_framework import viewsets, permissions, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]  # Пока без авторизации


class LessonListView(generics.ListAPIView):
    """
    Generic-класс для получения списка уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonRetrieveView(generics.RetrieveAPIView):
    """
    Generic-класс для получения одного урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonCreateView(generics.CreateAPIView):
    """
    Generic-класс для создания урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonUpdateView(generics.UpdateAPIView):
    """
    Generic-класс для изменения урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonDestroyView(generics.DestroyAPIView):
    """
    Generic-класс для удаления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]