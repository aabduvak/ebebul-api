from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate

from .models import User, Video, Hospital

@receiver(post_save, sender=User)
def set_default_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='User'))

class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for creating a new auth token for a user
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Check if the email and password are valid
        if email and password:
            # Get the user object for the given email
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            
            # Raise an error if the user is not found or the password is incorrect
            if not user:
                raise serializers.ValidationError({"auth_token": None}, code='authorization')
                
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return token.key


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