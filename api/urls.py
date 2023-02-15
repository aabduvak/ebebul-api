from django.urls import path, include
from .views import UserAPIViewSet, ValidateUser
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserAPIViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
	path('validate/', ValidateUser.as_view())
]
