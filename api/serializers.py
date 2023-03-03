from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
        User, 
        Video,
        Hospital,
        Notification,
        Content,
        VisitRequest
    )

@receiver(post_save, sender=User)
def set_default_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='User'))

class UserSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'is_active', 'user_permissions')
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
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            birth_date=validated_data['birth_date'],
            address=validated_data['address']
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
        fields = '__all__'

class VisitRequestSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    
    class Meta:
        model = VisitRequest
        fields = '__all__'