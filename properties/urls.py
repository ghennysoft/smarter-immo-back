from django.urls import path
from .views import PropertyViewSet

urlpatterns = [
    path('property/', PropertyViewSet.as_view(), name='property'),
]
