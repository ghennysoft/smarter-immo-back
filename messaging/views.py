from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from accounts.models import CustomUser
from properties.models import Property


class ConversationListView(generics.ListCreateAPIView):
    """List user's conversations or start a new one."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.all()

    def create(self, request, *args, **kwargs):
        recipient_id = request.data.get('recipient_id')
        property_id = request.data.get('property_id')

        if not recipient_id:
            return Response({'error': 'recipient_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipient = CustomUser.objects.get(id=recipient_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if recipient == request.user:
            return Response({'error': 'Cannot message yourself'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate property if provided
        prop = None
        if property_id:
            try:
                prop = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                pass

        # Check if a conversation already exists between these two users for this property
        existing = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=recipient
        )
        if prop:
            existing = existing.filter(property=prop)
        else:
            existing = existing.filter(property__isnull=True)

        existing = existing.first()

        if existing:
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        conversation = Conversation.objects.create(property=prop)
        conversation.participants.add(request.user, recipient)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageListView(generics.ListAPIView):
    """List messages in a conversation."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Mark unread messages as read
        queryset.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SendMessageView(generics.CreateAPIView):
    """Send a message in a conversation."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        conversation = Conversation.objects.get(
            id=conversation_id,
            participants=self.request.user
        )
        message = serializer.save(sender=self.request.user, conversation=conversation)
        conversation.save()  # Update updated_at
        # Create notification for the other participant
        from accounts.models import Notification
        for participant in conversation.participants.exclude(id=self.request.user.id):
            Notification.objects.create(
                recipient=participant,
                notification_type='message',
                title=f'Message de {self.request.user.first_name} {self.request.user.last_name}',
                message=message.content[:100],
                link=f'/messages?conversation={conversation.id}',
            )
