import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import CustomUser


@pytest.mark.django_db
class TestAuthEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@test.com',
            'phone': '+243999000001',
            'gender': 'M',
            'password': 'TestPass123!',
        }
        self.user = CustomUser.objects.create_user(
            email='existing@test.com',
            password='TestPass123!',
            first_name='Existant',
            last_name='User',
            phone='+243999000000',
            gender='M',
        )

    def test_register_success(self):
        response = self.client.post('/api/accounts/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='jean@test.com').exists())

    def test_register_duplicate_email(self):
        data = {**self.user_data, 'email': 'existing@test.com', 'phone': '+243999000002'}
        response = self.client.post('/api/accounts/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        response = self.client.post('/api/accounts/token/', {
            'email': 'existing@test.com',
            'password': 'TestPass123!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        response = self.client.post('/api/accounts/token/', {
            'email': 'existing@test.com',
            'password': 'WrongPassword',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/accounts/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'existing@test.com')

    def test_profile_unauthenticated(self):
        response = self.client.get('/api/accounts/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        login_resp = self.client.post('/api/accounts/token/', {
            'email': 'existing@test.com',
            'password': 'TestPass123!',
        }, format='json')
        refresh_token = login_resp.data['refresh']
        response = self.client.post('/api/accounts/token/refresh/', {
            'refresh': refresh_token,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_password_reset_request(self):
        response = self.client.post('/api/accounts/password-reset/', {
            'email': 'existing@test.com',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/api/accounts/profile-edit/', {
            'first_name': 'NouveauNom',
            'last_name': 'User',
            'email': 'existing@test.com',
            'phone': '+243999000000',
            'gender': 'M',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NouveauNom')
