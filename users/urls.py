from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserPaymentHistoryView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:id>/payment-history/', UserPaymentHistoryView.as_view(), name='user-payment-history'),
]
