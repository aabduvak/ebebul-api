from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from .models import (
        User, 
        Video,
        Hospital,
        Notification,
        Content,
        Appointment
    )

class UserSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        # Call the parent class's update() method to update the other fields
        instance = super().update(instance, validated_data)

        # If the password field is present in the request, encrypt it and save it to the instance
        if password is not None:
            instance.set_password(password)
            instance.save()
        
        return instance
    
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            birth_date=validated_data['birth_date'],
            address=validated_data['address'],
            category=validated_data['category'],
            longitude=validated_data['longitude'],
            latitude=validated_data['latitude'],
            marial_status=validated_data['marial_status']
        )
        
        if user:
            user.set_password(user.password)
            user.save()
        return user


class VideoSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = Video
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = Hospital
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    
    class Meta:
        model = Notification
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    
    class Meta:
        model = Content
        exclude = ('file',)

class AppointmentSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    
    class Meta:
        model = Appointment
        fields = '__all__'