from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListView,
    LessonRetrieveView,
    LessonCreateView,
    LessonUpdateView,
    LessonDestroyView,
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
]
