from rest_framework import serializers
from .models import FinUser
import random
import re
from rest_framework_simplejwt.tokens import RefreshToken
from .validators import custom_email_validator as email_valid


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FinUser
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'image']


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200)    
    last_name = serializers.CharField(max_length=200)    
    email = serializers.EmailField()    
    password = serializers.CharField(max_length=20)
    
        
    def validate(self, attrs):
        email = attrs['email']
        data = FinUser.objects.filter(email=attrs['email']).first()
        if not email_valid(email):
                    raise serializers.ValidationError({"Error": "Email address isn't valid"})
        if data:
                    raise serializers.ValidationError({'Error': 'Email is already used'})
        return attrs
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()    
    password = serializers.CharField(max_length=20)    


    def validate(self, attrs):
        data = FinUser.objects.filter(email=attrs['email']).first()
        if not data:
                    raise serializers.ValidationError({'Error': 'User not registered'})
        if not data.check_password(attrs['password']):
            
                    raise serializers.ValidationError({'Error': 'Wrong password'})
        return attrs

    def save(self):
        print(self.validated_data)
        user = FinUser.objects.get(email=self.validated_data['email'])
        token = get_tokens_for_user(user)
        return token

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['token'] = get_tokens_for_user(instance)
        
        return 