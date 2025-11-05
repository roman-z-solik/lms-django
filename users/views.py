from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserPaymentHistorySerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с платежами (Задание 4)
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']  # Сортировка по умолчанию: новые платежи first


class UserPaymentHistoryView(generics.RetrieveAPIView):
    """
    API для получения истории платежей пользователя (Дополнительное задание)
    """
    queryset = User.objects.all()
    serializer_class = UserPaymentHistorySerializer
    lookup_field = 'id'

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Добро пожаловать в LMS API!',
        'endpoints': {
            'courses': '/api/materials/courses/',
            'lessons_list': '/api/materials/lessons/',
            'lesson_create': '/api/materials/lessons/create/',
            'payments': '/api/users/payments/',
            'user_payment_history': '/api/users/users/{id}/payment-history/',
            'admin': '/admin/',
            'api_auth': '/api-auth/'
        }
    })
