from django.urls import path
from .views import PropertyList, PropertyListView, MyPropertyList, PropertyDetail

urlpatterns = [
    path('property-list/', PropertyListView.as_view(), name='property-list'),
    path('properties/', PropertyList.as_view(), name='properties'),
    path('properties/', PropertyList.as_view(), name='properties'),
    path('myProperties/', MyPropertyList.as_view(), name='myProperties'),
    path('property/<int:pk>/', PropertyDetail.as_view(), name='property'),
]
