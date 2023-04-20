from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserAPIViewSet,
    VideoAPIViewSet,
    HospitalAPIViewSet,
    UserCreateView,
    UserRUDView,
    AuthTokenPairView,
    NotificationAPIViewSet,
    ContentAPIViewSet,
    AppointmentAPIViewSet,
    ContentFileAPIView,
    GetCityAPI,
    GetDisctrictAPI, # never use again
    CityViewSet,
    DistrictViewSet
)

router = SimpleRouter()
router.register(r'users', UserAPIViewSet, basename='user')
router.register(r'videos', VideoAPIViewSet, basename='video')
router.register(r'hospitals', HospitalAPIViewSet, basename='hospital')
router.register(r'notifications', NotificationAPIViewSet, basename='notification')
router.register(r'contents', ContentAPIViewSet, basename='content')
router.register(r'visits', AppointmentAPIViewSet, basename='visit')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'districts', DistrictViewSet, basename='district')

urlpatterns = [
    path('', include(router.urls)),
    path('contents/<int:id>/file/', ContentFileAPIView.as_view(), name='content-file'),
    path('auth/users/', UserCreateView.as_view()),
    path('auth/users/me/', UserRUDView.as_view()),
    path('auth/token/login/', AuthTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('update/city/', GetCityAPI.as_view(), name='update-city'),
    # path('update/district/', GetDisctrictAPI.as_view(), name='update-district'),
]
