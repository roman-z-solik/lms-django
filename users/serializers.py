from rest_framework import serializers
from .models import Payment, User
from materials.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment (Задание 4)
    """
    user_email = serializers.CharField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='paid_course.title', read_only=True)
    lesson_title = serializers.CharField(source='paid_lesson.title', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'payment_date', 'paid_course',
            'course_title', 'paid_lesson', 'lesson_title', 'amount',
            'payment_method', 'payment_method_display'
        ]
        read_only_fields = ['id', 'payment_date', 'user_email', 'course_title', 'lesson_title', 'payment_method_display']


class UserPaymentHistorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода истории платежей пользователя (Дополнительное задание)
    """
    payments = PaymentSerializer(many=True, read_only=True)
    total_payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'payments', 'total_payments']

    def get_total_payments(self, obj):
        """Общая сумма всех платежей пользователя"""
        return obj.payments.aggregate(total=models.Sum('amount'))['total'] or 0