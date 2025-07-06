from rest_framework_simplejwt.views import TokenRefreshView
from knox.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', views.UserProfile.as_view()),
    path('profile-edit/', views.EditProfile.as_view()),
]
