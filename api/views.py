from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly

class UserAPIViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


#class UserAPIUpdateViewSet(mixins.UpdateModelMixin,
#			   viewsets.GenericViewSet):
#	queryset = User.objects.all()
#	serializer_class = UserSerializer
#	permission_classes = [IsOwnerOrReadOnly]
