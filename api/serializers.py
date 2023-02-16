from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from .models import User

class UserSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'is_active', )
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        return user
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        return instance