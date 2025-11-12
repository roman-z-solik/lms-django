from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyTokenObtainPairView,
    UserViewSet,
    UserRegisterView,
    UserProfileView,
    UserDetailView,
    api_root,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", api_root, name="api-root"),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("users/<int:id>/", UserDetailView.as_view(), name="user-detail"),
]
