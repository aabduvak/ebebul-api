from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'users', UserAPIViewSet, basename='user')
router.register(r'videos', VideoAPIViewSet, basename='video')
router.register(r'hospitals', HospitalAPIViewSet, basename='hospital')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', AuthToken.as_view()),
    path('auth/token/logout/', RemoveAuthToken.as_view()),
    path('auth/users/', UserCreateView.as_view()),
    path('auth/users/me/', UserRUDView.as_view()),
    #path('users/<int:pk>', UserAPIUpdateViewSet.as_view({'put': 'update', 'put': 'partial_update'}))
]

# auth/users/me
