from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
# from rest_framework.exceptions import AuthenticationFailed


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.first_name
        token['firstname'] = user.first_name
        token['lastname'] = user.last_name
        token['email'] = user.email
        token['phone'] = user.phone
        token['gender'] = user.gender
        token['is_superuser'] = user.is_superuser
        token['image'] = user.image.url if user.image else None # Ou une url d'image par défaut
        # token['is_active'] = user.is_active
        # token['is_staff'] = user.is_staff
        # token['last_login'] = user.last_login
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', 'groups', 'user_permissions')
        read_only_fields = ['id']


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'gender', 'image')  # Utilisez les champs définis dans votre modèle User

    # def update(self, instance, validated_data):
    #     user = CustomUser.objects.update(
    #         email=validated_data['email'],
    #         first_name=validated_data.get('first_name'),
    #         last_name=validated_data.get('last_name'),
    #         phone=validated_data.get('phone'),
    #         gender=validated_data.get('gender'),
    #         image=validated_data.get('image'),
    #     )
    #     return user
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'gender', 'image', 'password')  # Utilisez les champs définis dans votre modèle User

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone=validated_data.get('phone'),
            gender=validated_data.get('gender'),
        )
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'image', 'first_name', 'last_name', 'phone', 'gender')
        # username et email peuvent être en read_only si vous ne voulez pas qu'ils soient modifiés ici
        # read_only_fields = ('username', 'email')
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')  # Utilisez les champs définis dans votre modèle User

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Remplissez tous les champs')

        user = authenticate(email=email, password=password)
        print(f'serializer: {user}')

        if user is None:
            raise serializers.ValidationError("Invalid credentials, try again")

        attrs['user'] = user
        return attrs
