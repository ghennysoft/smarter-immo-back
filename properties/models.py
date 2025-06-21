from django.db import models
from accounts.models import CustomUser


class Property(models.Model):
    PROPERTY_TYPES = [
        ('HOUSE', 'Maison'),
        ('APARTMENT', 'Appartement'),
        ('VILLA', 'Villa'),
        ('LAND', 'Terrain'),
        ('COMMERCIAL', 'Local commercial'),
    ]

    ANNONCE_TYPES = [
        ('SALE', 'À vendre'),
        ('RENT', 'À louer'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='property/')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    annonce_type = models.CharField(max_length=20, choices=ANNONCE_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.property.title}'

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
