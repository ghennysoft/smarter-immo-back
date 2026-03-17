from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Property, Favorite
from .serializers import PropertySerializer, FavoriteSerializer


class PropertyListView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'property_type', 'annonce_type']
    search_fields = ['title', 'description', 'city', 'address']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']


class PropertyList(APIView):
    def get(self, request):
        properties = Property.objects.all()

        city = request.query_params.get('city')
        property_type = request.query_params.get('property_type')
        annonce_type = request.query_params.get('annonce_type')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search = request.query_params.get('search')

        if city:
            properties = properties.filter(city__icontains=city)
        if property_type:
            properties = properties.filter(property_type=property_type)
        if annonce_type:
            properties = properties.filter(annonce_type=annonce_type)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if search:
            properties = properties.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(city__icontains=search) |
                Q(address__icontains=search)
            )

        serializer = PropertySerializer(properties, many=True, context={'request': request})
        return Response(serializer.data, status=200)
    
    def post(self, request):
        serializer = PropertySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MyPropertyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Property.objects.filter(owner=self.request.user)
        serializer = PropertySerializer(properties, many=True, context={'request': request})
        return Response(serializer.data, status=200)


class PropertyDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Property, pk=pk)
    
    def get(self, request, pk):
        property = self.get_object(pk)
        serializer = PropertySerializer(property, context={'request': request})
        return Response(serializer.data, status=200)
    
    def put(self, request, pk):
        property = self.get_object(pk)
        if property.owner != request.user:
            return Response({'error': 'Non autorisé'}, status=403)
        serializer = PropertySerializer(property, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        property = self.get_object(pk)
        if property.owner != request.user:
            return Response({'error': 'Non autorisé'}, status=403)
        property.delete()
        return Response(status=204)


class FavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related('property')
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        property_id = request.data.get('property_id')
        if not property_id:
            return Response({'error': 'property_id requis'}, status=400)
        
        property_obj = get_object_or_404(Property, pk=property_id)

        favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_obj)
        if not created:
            favorite.delete()
            return Response({'status': 'removed'})
        
        return Response({'status': 'added'}, status=201)
        