
from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404

from .calc import get_nearest_data

from .serializers import (
        UserSerializer, 
        VideoSerializer, 
        HospitalListSerializer,
        HospitalDetailSerializer,
        NotificationSerializer,
        ContentSerializer,
        AppointmentSerializer,
        CitySerializer,
        DisctrictSerializer,
        MidwifeListSerializer
    )
from .models import (
        User, 
        Video,
        Hospital,
        Notification,
        Content,
        Appointment,
        City,
        Discrict
    )

from .data import NosyAPI

class ContentFileAPIView(View):
    def get(self, request, id):
        item = get_object_or_404(Content, pk=id)
        with open(item.file.path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')

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


class NotificationAPIViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class ContentAPIViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

class AppointmentAPIViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

class HospitalAPIViewSet(mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalDetailSerializer
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
        
        protocol = request.scheme

        # Get the domain name from the request
        domain = request.META['HTTP_HOST']

        # Construct the base URL using the protocol and domain
        base_url = f"{protocol}://{domain}"
        
        if not user:
            return Response({'error': 'user not found'}, status=404)
        return Response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'birth_date': user.birth_date,
            'address': user.address,
            'gender': user.gender,
            'identity_number': user.identity_number,
            'weight': user.weight,
            'height': user.height,
            'last_login': user.last_login,
            'longitude': user.longitude,
            'latitude': user.latitude,
            'marial_status': user.marial_status,
            'profile': base_url + user.photo.url,
            'category_name': user.category.name,
            'category_id': user.category.id
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

class GetCityAPI(APIView):
    def get(self, request):
        api = NosyAPI()
        
        response = api.store_city()
        
        return response


class GetDisctrictAPI(APIView):
    def get(self, request):
        api = NosyAPI()
        
        cities = City.objects.all()
        
        try:
            for city in cities:
                api.store_discrict(city)
        except:
            return Response({'status': 500, 'message': 'failed'})
        return Response({'status': 200, 'message': 'ok'})


class GetHospitalAPI(APIView):
    def get(self, request):
        api = NosyAPI()
        
        cities = City.objects.all()
        
        try:
            for city in cities:
                api.store_hospitals(city)
        except:
            return Response({'status': 500, 'message': 'failed'})
        return Response({'status': 200, 'message': 'ok'})


class CityViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]
    
class DistrictViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Discrict.objects.all()
    serializer_class = DisctrictSerializer
    permission_classes = [IsAdminUser]

class NearestHospitalsView(APIView):
    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if not latitude or not longitude:
            return Response({'error': 'Latitude and longitude are required.'}, status=400)

        try:
            user_latitude = float(latitude)
            user_longitude = float(longitude)
        except ValueError:
            return Response({'error': 'Invalid latitude or longitude.'}, status=400)

        hospitals = get_nearest_data(user_latitude, user_longitude, Hospital)

        serializer = HospitalListSerializer(hospitals, many=True, context={'user_latitude': user_latitude, 'user_longitude': user_longitude})
        
        return Response({'hospitals': serializer.data}, status=200)

class NearestMidwifeView(APIView):
    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if not latitude or not longitude:
            return Response({'error': 'Latitude and longitude are required.'}, status=400)

        try:
            user_latitude = float(latitude)
            user_longitude = float(longitude)
        except ValueError:
            return Response({'error': 'Invalid latitude or longitude.'}, status=400)

        users = get_nearest_data(user_latitude, user_longitude, User, True)

        serializer = MidwifeListSerializer(users, many=True, context={'user_latitude': user_latitude, 'user_longitude': user_longitude})
        
        return Response({'hospitals': serializer.data}, status=200)