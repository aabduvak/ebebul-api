from django.urls import path, include
from .views import UserAPIViewSet, AuthToken, RemoveAuthToken
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'users', UserAPIViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', AuthToken.as_view()),
    path('auth/token/logout/', RemoveAuthToken.as_view())
    #path('users/<int:pk>', UserAPIUpdateViewSet.as_view({'put': 'update', 'put': 'partial_update'}))
]
