from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender = models.CharField(max_length=1)
    last_active = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD  = 'email'

    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    @property
    def is_online(self):
        if not self.last_active:
            return False
        return (timezone.now() - self.last_active).total_seconds() < 300  # 5 min

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Notification(models.Model):
    TYPES = (
        ('message', 'Nouveau message'),
        ('property', 'Propriété'),
        ('system', 'Système'),
    )
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPES, default='system')
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.notification_type}: {self.title}'
    