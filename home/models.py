from django.db import models
from accounts.models import CustomUser

class Residency(models.Model):
    author = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, blank = True, null = True)
    title = models.CharField(max_length = 500)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    address = models.CharField(max_length = 500)
    bed_rooms = models.CharField(max_length = 2)
    bath_rooms = models.CharField(max_length = 2)
    parking = models.CharField(max_length = 2)
    city = models.CharField(max_length = 500)
    country = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    # Category and Type = ChoiceField

    def __str__(self):
        return self.title
    

class Chapitre(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    cour = models.ForeignKey(Cour, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
