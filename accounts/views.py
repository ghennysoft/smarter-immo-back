from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import CustomUser
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, EditUserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, LoginSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


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


# class UserProfileView(generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def get_object(self):
#         return self.request.user

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
        
#         if getattr(instance, '_prefetched_objects_cache', None):
#             instance._prefetched_objects_cache = {}
            
#         # Après mise à jour, on retourne un nouveau token avec les données mises à jour
#         refresh = RefreshToken.for_user(instance)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': serializer.data
#         })