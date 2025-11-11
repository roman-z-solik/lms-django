from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListView,
    LessonRetrieveView,
    LessonCreateView,
    LessonUpdateView,
    LessonDestroyView,
    PaymentCreateView,
    PaymentStatusView,
    PaymentSuccessView,
    PaymentCancelView,
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
    path("lessons/create/", LessonCreateView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonRetrieveView.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/update/", LessonUpdateView.as_view(), name="lesson-update"),
    path("lessons/<int:pk>/delete/", LessonDestroyView.as_view(), name="lesson-delete"),
    path("payments/create/", PaymentCreateView.as_view(), name="payment-create"),
    path(
        "payments/<int:pk>/status/", PaymentStatusView.as_view(), name="payment-status"
    ),
    path(
        "payments/success/<str:pk>/",
        PaymentSuccessView.as_view(),
        name="payment-success",
    ),
    path("payments/cancel/", PaymentCancelView.as_view(), name="payment-cancel"),
]
