import pytest
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import CustomUser
from properties.models import Property, Favorite
from io import BytesIO
from PIL import Image


def create_test_image():
    img = Image.new('RGB', (100, 100), color='red')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    return SimpleUploadedFile('test.jpg', buf.read(), content_type='image/jpeg')


@pytest.mark.django_db
class TestPropertyEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='owner@test.com',
            password='TestPass123!',
            first_name='Owner',
            last_name='User',
            phone='+243999000010',
            gender='M',
        )
        self.other_user = CustomUser.objects.create_user(
            email='other@test.com',
            password='TestPass123!',
            first_name='Other',
            last_name='User',
            phone='+243999000011',
            gender='F',
        )
        self.property = Property.objects.create(
            title='Maison Test',
            description='Description test',
            main_image=create_test_image(),
            price=100000,
            city='Kinshasa',
            address='123 Avenue Test',
            property_type='maison',
            annonce_type='À vendre',
            long=20,
            larg=15,
            bedrooms=3,
            bathrooms=2,
            equipments='Piscine, Jardin',
            owner=self.user,
        )

    def test_list_properties(self):
        response = self.client.get('/api/property-list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_property_detail(self):
        response = self.client.get(f'/api/property/{self.property.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Maison Test')

    def test_create_property_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Nouvelle Propriété',
            'description': 'Description',
            'main_image': create_test_image(),
            'price': 200000,
            'city': 'Lubumbashi',
            'address': '456 Avenue Nouvelle',
            'property_type': 'appartement',
            'annonce_type': 'À louer',
            'long': 10,
            'larg': 8,
            'bedrooms': 2,
            'bathrooms': 1,
            'equipments': 'Cuisine',
        }
        response = self.client.post('/api/properties/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_property_by_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/property/{self.property.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_property_by_non_owner(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/api/property/{self.property.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_properties(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/myProperties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_city(self):
        response = self.client.get('/api/properties/?city=Kinshasa')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_price_range(self):
        response = self.client.get('/api/properties/?min_price=50000&max_price=150000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestFavoriteEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='favuser@test.com',
            password='TestPass123!',
            first_name='Fav',
            last_name='User',
            phone='+243999000020',
            gender='M',
        )
        self.property = Property.objects.create(
            title='Propriété Favorite',
            description='Test',
            main_image=create_test_image(),
            price=150000,
            city='Kinshasa',
            address='Test Address',
            property_type='villa',
            annonce_type='À vendre',
            long=30,
            larg=20,
            bedrooms=4,
            bathrooms=3,
            equipments='Piscine',
            owner=self.user,
        )

    def test_add_favorite(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/favorites/', {'property_id': self.property.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'added')

    def test_remove_favorite(self):
        self.client.force_authenticate(user=self.user)
        Favorite.objects.create(user=self.user, property=self.property)
        response = self.client.post('/api/favorites/', {'property_id': self.property.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'removed')

    def test_list_favorites(self):
        self.client.force_authenticate(user=self.user)
        Favorite.objects.create(user=self.user, property=self.property)
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_favorites_unauthenticated(self):
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
