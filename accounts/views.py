from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, LoginSerializer

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

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
            return Response(response.data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_404_BAD_REQUEST)


@api_view()
@permission_classes([AllowAny])
def profile(request):
    if request.method == 'GET':
        response = f"Hey {request.user}, You are seeing a GET response"
        return Response({'response': response, 'response2': 'Other thing'}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_404_BAD_REQUEST) 
