from rest_framework import serializers
from .models import Property, PropertyImage, Favorite
from accounts.serializers import UserSerializer

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('id', 'image')

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    # is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'

    read_only_fields = ['owner', 'created_at', 'updated_at']

    # def get_is_favorite(self, obj):
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         return Favorite.objects.filter(user=request.user, property=obj).exists()
    #     return False

    def create(self, validated_data):
        # uploaded_images = validated_data.pop('uploaded_images')
        property = Property.objects.create(**validated_data)
        # for image_file in uploaded_images:
        #     PropertyImage.objects.create(property=property, image=image_file)
        return property

class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'property', 'created_at')