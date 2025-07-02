from django.urls import path
from .views import PropertyList, MyPropertyList, PropertyDetail

urlpatterns = [
    path('properties/', PropertyList.as_view(), name='properties'),
    path('myProperties/', MyPropertyList.as_view(), name='myProperties'),
    path('property/<int:pk>/', PropertyDetail.as_view(), name='property'),
]
