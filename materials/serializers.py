from rest_framework import serializers
from .models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "price",
            "owner",
            "created_at",
            "updated_at",
            "lessons_count",
            "lessons",
        ]

    def get_lessons_count(self, obj):
        """
        Метод для получения количества уроков в курсе.
        obj - экземпляр модели Course
        """
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_email",
            "course",
            "course_title",
            "amount",
            "status",
            "payment_url",
            "stripe_session_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "amount",
            "status",
            "payment_url",
            "stripe_session_id",
            "created_at",
            "updated_at",
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Payment
        fields = ["course_id"]

    def create(self, validated_data):
        return validated_data
      