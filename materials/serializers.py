from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'created_at',
                 'updated_at', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        """
        Метод для получения количества уроков в курсе.
        obj - экземпляр модели Course
        """
        return obj.lessons.count()
