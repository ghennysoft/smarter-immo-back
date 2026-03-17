from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('profile/', views.UserProfile.as_view()),
    path('profile-edit/', views.EditProfile.as_view()),
    path('user/<int:pk>/', views.PublicProfileView.as_view()),
    path('heartbeat/', views.HeartbeatView.as_view()),
    path('notifications/', views.NotificationListView.as_view()),
    path('notifications/read/', views.NotificationMarkReadView.as_view()),
    path('notifications/<int:pk>/read/', views.NotificationMarkReadView.as_view()),
    path('password-reset/', views.PasswordResetRequestView.as_view()),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view()),
]
