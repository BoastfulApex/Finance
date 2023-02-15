from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    queryset = FinUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            finuser = FinUser.objects.create(
                email=serializer.validated_data['email'],
            )
            finuser.last_name=serializer.validated_data['last_name']
            finuser.first_name=serializer.validated_data['first_name']
            finuser.set_password(serializer.validated_data['password'])
            finuser.save()
            token = get_tokens_for_user(finuser)
            user = {
                "id": finuser.id,
                "first_name": finuser.first_name,
                "last_name": finuser.last_name,
                "email": finuser.email,
            }
            token['user'] = user
            return Response(token)


class LoginView(generics.CreateAPIView):
    queryset = FinUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            finuser = FinUser.objects.get(email=serializer.validated_data['email'])
            token = get_tokens_for_user(finuser)
            user = {
                "id": finuser.id,
                "first_name": finuser.first_name,
                "last_name": finuser.last_name,
                "email": finuser.email,
            }
            token['user'] = user
            return Response(token)
    
        
