from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import (
    PaymentSerializer, UserPaymentHistorySerializer,
    UserSerializer, UserRegisterSerializer, MyTokenObtainPairSerializer
)


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
    """Профиль текущего пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с платежами (Задание 4)
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']


class UserPaymentHistoryView(generics.RetrieveAPIView):
    """
    API для получения истории платежей пользователя (Дополнительное задание)
    """
    queryset = User.objects.all()
    serializer_class = UserPaymentHistorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Добро пожаловать в LMS API!',
        'endpoints': {
            'register': '/api/users/register/',
            'token': '/api/users/token/',
            'token_refresh': '/api/users/token/refresh/',
            'profile': '/api/users/profile/',
            'users': '/api/users/users/',
            'payments': '/api/users/payments/',
            'user_payment_history': '/api/users/users/{id}/payment-history/',
            'courses': '/api/materials/courses/',
            'lessons': '/api/materials/lessons/',
            'admin': '/admin/',
            'api_auth': '/api-auth/'
        }
    })
