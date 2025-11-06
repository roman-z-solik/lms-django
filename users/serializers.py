from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum
from .models import Payment, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "avatar"]
        read_only_fields = ["id"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone",
            "city",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра собственного профиля (полная информация)
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "date_joined",
        ]
        read_only_fields = ["id", "email", "date_joined"]


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра чужого профиля (только общая информация)
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "city", "avatar", "date_joined"]
        read_only_fields = [
            "id",
            "email",
            "first_name",
            "city",
            "avatar",
            "date_joined",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    course_title = serializers.CharField(source="paid_course.title", read_only=True)
    lesson_title = serializers.CharField(source="paid_lesson.title", read_only=True)
    payment_method_display = serializers.CharField(
        source="get_payment_method_display", read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_email",
            "payment_date",
            "paid_course",
            "course_title",
            "paid_lesson",
            "lesson_title",
            "amount",
            "payment_method",
            "payment_method_display",
        ]
        read_only_fields = [
            "id",
            "payment_date",
            "user_email",
            "course_title",
            "lesson_title",
            "payment_method_display",
        ]


class UserPaymentHistorySerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    total_payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "payments",
            "total_payments",
        ]

    def get_total_payments(self, obj):
        """Общая сумма всех платежей пользователя"""
        return obj.payments.aggregate(total=Sum("amount"))["total"] or 0
