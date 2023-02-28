from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Video, Hospital
from .serializers import UserSerializer, VideoSerializer, HospitalSerializer

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

class HospitalAPIViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
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
        }, status=200)
    
    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            user.delete()

            return Response({'message': 'User successfully deleted.'}, status=200)
        except Token.DoesNotExist:
            # If the token doesn't exist, return an error message
            return Response({'message': 'No auth token found for the current user.'}, status=400)
        
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class AuthTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except:
            return Response({'detail':'invalid email or password', 'access': None, 'refresh': None}, status=status.HTTP_401_UNAUTHORIZED)
