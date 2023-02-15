from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ValidateUser(APIView):
    def get(self, request, *args, **kwargs):
        pass
    
    def post(self, request):
        user = User.objects.get(email=request.POST.get('email'))
        
        is_valid = user.check_password(request.POST.get('password'))
        
        return Response(data={"is_valid": is_valid}, status=status.HTTP_200_OK)