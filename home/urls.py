from django.contrib import admin
from django.urls import path
from .views import CourView, CourDetail

urlpatterns = [
    path('cours/', CourView.as_view()),
    path('cours/<int:pk>/', CourDetail.as_view()),
]
