from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from users.models import User
from users.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    MyTokenObtainPairSerializer,
    UserProfileSerializer,
    UserPublicSerializer,
)
from users.permissions import IsOwner


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций с пользователями"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профиль текущего пользователя (полная информация)"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """Просмотр профиля любого пользователя (ограниченная информация)"""

    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


@swagger_auto_schema(
    method="get",
    operation_description="Получение корневой страницы API со списком доступных эндпоинтов",
    operation_summary="Корневой эндпоинт API",
    tags=["API"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    """
    Корневой эндпоинт API LMS платформы.
    Возвращает список доступных эндпоинтов системы.
    """
    return Response(
        {
            "message": "Добро пожаловать в LMS API!",
            "endpoints": {
                "register": "/api/users/register/",
                "token": "/api/users/token/",
                "token_refresh": "/api/users/token/refresh/",
                "my_profile": "/api/users/profile/",
                "user_detail": "/api/users/users/{id}/",
                "users": "/api/users/users/",
                "courses": "/api/materials/courses/",
                "lessons": "/api/materials/lessons/",
                "payments": "/api/materials/payments/",
                "subscriptions": "/api/materials/subscriptions/",
                "admin": "/admin/",
                "api_auth": "/api-auth/",
                "swagger_docs": "/swagger/",
                "redoc_docs": "/redoc/",
            },
        }
    )
  