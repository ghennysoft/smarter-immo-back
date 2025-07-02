from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender = models.CharField(max_length=1)

    USERNAME_FIELD  = 'email'

    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    