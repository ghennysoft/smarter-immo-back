from django.db import models
from accounts.models import CustomUser


class Property(models.Model):
    PROPERTY_TYPES = [
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('studio', 'studio'),
        ('villa', 'Villa'),
        ('terrain', 'Terrain'),
        ('commercial', 'Local commercial'),
    ]

    ANNONCE_TYPES = [
        ('À vendre', 'À vendre'),
        ('À louer', 'À louer'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    main_image = models.ImageField(upload_to='images/properties/')

    price = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    annonce_type = models.CharField(max_length=20, choices=ANNONCE_TYPES)

    long = models.IntegerField()
    larg = models.IntegerField()

    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    equipments = models.TextField()

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.owner}'

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/properties/')

    def __str__(self):
        return f'{self.property.title}'

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
