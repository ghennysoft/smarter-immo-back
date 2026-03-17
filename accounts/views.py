from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import CustomUser, Notification
from django.contrib.auth import authenticate
from .serializers import UserSerializer, EditUserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, NotificationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone

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
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=200)
    
    def put(self, request):
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
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
        serializer = EditUserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        user.delete()
        return Response(status=204)


class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        from .serializers import PublicUserSerializer
        serializer = PublicUserSerializer(user, context={'request': request})
        data = serializer.data
        # Include user's properties
        from properties.serializers import PropertySerializer
        from properties.models import Property
        properties = Property.objects.filter(owner=user)
        data['properties'] = PropertySerializer(properties, many=True, context={'request': request}).data
        return Response(data)


class HeartbeatView(APIView):
    """Update user's last_active timestamp."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.last_active = timezone.now()
        request.user.save(update_fields=['last_active'])
        # Return unread messages count + unread notifications count
        from messaging.models import Message
        unread_messages = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()
        unread_notifications = request.user.notifications.filter(is_read=False).count()
        return Response({
            'unread_messages': unread_messages,
            'unread_notifications': unread_notifications,
        })


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = request.user.notifications.all()[:50]
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        if pk:
            notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
            notif.is_read = True
            notif.save(update_fields=['is_read'])
        else:
            request.user.notifications.filter(is_read=False).update(is_read=True)
        return Response({'status': 'ok'})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.core.mail import send_mail
        from django.conf import settings

        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email requis'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Si cet email existe, un lien de réinitialisation a été envoyé.'})

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"{request.data.get('frontend_url', 'http://localhost:5173')}/reset-password/{uid}/{token}"

        send_mail(
            'Réinitialisation de mot de passe - Smarter Immo',
            f'Cliquez sur ce lien pour réinitialiser votre mot de passe:\n\n{reset_url}',
            settings.EMAIL_HOST_USER or 'noreply@smarterimmo.com',
            [email],
            fail_silently=True,
        )

        return Response({'message': 'Si cet email existe, un lien de réinitialisation a été envoyé.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode

        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not all([uid, token, password]):
            return Response({'error': 'Tous les champs sont requis'}, status=400)

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(pk=user_id)
        except (CustomUser.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Lien invalide'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Lien expiré ou invalide'}, status=400)

        user.set_password(password)
        user.save()
        return Response({'message': 'Mot de passe réinitialisé avec succès'})