from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, AuthTokenSerializer
from .permissions import IsOwnerOrReadOnly

class UserAPIViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

#class UserAPIUpdateViewSet(mixins.UpdateModelMixin,
#			   viewsets.GenericViewSet):
#	queryset = User.objects.all()
#	serializer_class = UserSerializer
#	permission_classes = [IsOwnerOrReadOnly]

class AuthToken(ObtainAuthToken):

    serializer_class = AuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            token = serializer.save()
            return Response({'auth_token': token})
        return Response({'auth_token': None}, status=401)

class RemoveAuthToken(APIView):
    """
    View for removing the auth token of the current user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Get the auth token associated with the current user's session
            token = Token.objects.get(user=request.user)

            # Delete the auth token
            token.delete()

            return Response({'message': 'Auth token successfully removed.'}, status=200)
        except Token.DoesNotExist:
            # If the token doesn't exist, return an error message
            return Response({'message': 'No auth token found for the current user.'}, status=400)