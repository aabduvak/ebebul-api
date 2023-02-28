from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserAPIViewSet,
    VideoAPIViewSet,
    HospitalAPIViewSet,
    UserCreateView,
    UserRUDView,
    AuthTokenPairView
)

router = SimpleRouter()
router.register(r'users', UserAPIViewSet, basename='user')
router.register(r'videos', VideoAPIViewSet, basename='video')
router.register(r'hospitals', HospitalAPIViewSet, basename='hospital')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/users/', UserCreateView.as_view()),
    path('auth/users/me/', UserRUDView.as_view()),
    path('auth/token/login/', AuthTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
