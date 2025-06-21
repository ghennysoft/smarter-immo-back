from rest_framework import serializers
from .models import Cour

class CourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cour
        fields = ["author", "title", "details", "skills", "price", "duration", "created_at"]