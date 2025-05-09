from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..factories import UserFactory

User = get_user_model()

class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.profile_url = reverse('profile')

        self.user = UserFactory.build()
        self.valid_registration_data = {
            'email': self.user.email,
            'username': self.user.username,
            'password': 'Testpass123!',
            'password2': 'Testpass123!',
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone': self.user.phone
        }

        self.existing_user = UserFactory(password='Testpass123!')

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.valid_registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.valid_registration_data['email']).exists())

    def test_user_registration_duplicate_email(self):
        # First registration
        self.client.post(self.register_url, self.valid_registration_data)
        
        # Try to register with same email
        response = self.client.post(self.register_url, self.valid_registration_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_obtain_pair(self):
        login_data = {
            'email': self.existing_user.email,
            'password': 'Testpass123!'
        }
        response = self.client.post(self.token_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_token_obtain_pair_invalid_credentials(self):
        login_data = {
            'email': self.existing_user.email,
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_retrieve(self):
        # Get token for authentication
        refresh = RefreshToken.for_user(self.existing_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.existing_user.email)
        self.assertEqual(response.data['username'], self.existing_user.username)

    def test_user_profile_update(self):
        # Get token for authentication
        refresh = RefreshToken.for_user(self.existing_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '9876543210'
        }

        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], update_data['first_name'])
        self.assertEqual(response.data['last_name'], update_data['last_name'])
        self.assertEqual(response.data['phone'], update_data['phone'])

    def test_user_profile_unauthorized(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)