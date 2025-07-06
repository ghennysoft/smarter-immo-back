from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Property, Favorite
from .serializers import PropertySerializer, FavoriteSerializer

class PropertyList(APIView):
    def get(self, request):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        print(request.data)
        serializer = PropertySerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MyPropertyList(APIView):
    def get(self, request):
        properties = Property.objects.filter(owner=self.request.user)
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=200)

class PropertyDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Property, pk=pk)
    
    def get(self, request, pk):
        property = self.get_object(pk)
        serializer = PropertySerializer(property)
        return Response(serializer.data, status=200)
    
    def put(self, request, pk):
        property = self.get_object(pk)
        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        property = self.get_object(pk)
        property.delete()
        return Response(status=204)
        