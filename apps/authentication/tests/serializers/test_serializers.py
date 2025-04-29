from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from apps.authentication.serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'Testpass123!',
            'password2': 'Testpass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890'
        }

    def test_valid_registration(self):
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertTrue(user.check_password(self.valid_data['password']))

    def test_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'DifferentPass123!'
        serializer = UserRegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_first_user_is_admin(self):
        # First user should be admin
        serializer = UserRegistrationSerializer(data=self.valid_data)
        serializer.is_valid()
        user = serializer.save()
        self.assertEqual(user.role, 'admin')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        # Subsequent users should be employees
        second_user_data = self.valid_data.copy()
        second_user_data['email'] = 'second@example.com'
        second_user_data['username'] = 'seconduser'
        serializer = UserRegistrationSerializer(data=second_user_data)
        serializer.is_valid()
        user = serializer.save()
        self.assertEqual(user.role, 'employee')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_weak_password(self):
        weak_password_data = self.valid_data.copy()
        weak_password_data['password'] = '123'
        weak_password_data['password2'] = '123'
        serializer = UserRegistrationSerializer(data=weak_password_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            phone='1234567890',
            role='employee'
        )

    def test_serialization(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['phone'], self.user.phone)
        self.assertEqual(data['role'], self.user.role)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_update(self):
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '9876543210'
        }
        serializer = UserSerializer(self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, update_data['first_name'])
        self.assertEqual(updated_user.last_name, update_data['last_name'])
        self.assertEqual(updated_user.phone, update_data['phone'])