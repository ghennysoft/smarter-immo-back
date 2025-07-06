from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import CustomUser
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, EditUserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, LoginSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from knox import views as knox_views


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
            return Response(response.data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_404_BAD_REQUEST)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
    def put(self, request):
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        user.delete()
        return Response(status=204)
   


class EditProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        serializer = EditUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        user.delete()
        return Response(status=204)
   
