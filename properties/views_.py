from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, Favorite
from .serializers import PropertySerializer, FavoriteSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().select_related('owner').prefetch_related('images')
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'annonce_type', 'city', 'bedrooms', 'bathrooms']
    search_fields = ['title', 'description', 'address', 'city']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        property = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            property=property
        )
        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'})
        return Response({'status': 'added to favorites'})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_properties(self, request):
        queryset = Property.objects.filter(created_by=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related('property')
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)


class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)