from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins

from .models import User, Video
from .serializers import UserSerializer, AuthTokenSerializer, VideoSerializer

class UserAPIViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAdminUser]


class VideoAPIViewSet(mixins.ListModelMixin,
					  mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
	queryset = Video.objects.all()
	serializer_class = VideoSerializer
	permission_classes = [IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

class UserRUDView(APIView):
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]
	
	def get(self, request):
		
		user = User.objects.get(email=request.user.email)
		
		if not user:
			return Response({'error': 'user not found'}, status=404)
		
		return Response({
			'id': user.id,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'email': user.email,
			'birth_date': user.birth_date,
			'address': user.address,
			'gender': user.gender,
			'identity_number': user.identity_number,
			'weight': user.weight,
			'height': user.height,
			'last_login': user.last_login
			#'groups': user.groups
		}, status=200)
	
	def delete(self, request, *args, **kwargs):
		try:
			# Get the auth token associated with the current user's session
			token = Token.objects.get(user=request.user)

			# Delete the user associated with the auth token
			user = token.user
			user.delete()

			# Delete the auth token
			token.delete()

			return Response({'message': 'User successfully deleted.'}, status=200)
		except Token.DoesNotExist:
			# If the token doesn't exist, return an error message
			return Response({'message': 'No auth token found for the current user.'}, status=400)
		
	def patch(self, request):
		token = Token.objects.get(user=request.user)
		
		instance = token.user
		serializer = UserSerializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data)

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

