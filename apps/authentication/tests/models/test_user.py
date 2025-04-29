from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'role': 'employee'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.role, self.user_data['role'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
            role='admin'  # Explicitly set role to admin
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.role, 'admin')

    def test_email_unique_constraint(self):
        # Create first user
        User.objects.create_user(**self.user_data)
        
        # Try to create user with same email
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)

    def test_is_admin_method(self):
        # Test for regular employee
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_admin())

        # Test for admin role
        admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
            role='admin'
        )
        self.assertTrue(admin_user.is_admin())

        # Test for staff user
        staff_user = User.objects.create_user(
            email='staff@example.com',
            username='staff',
            password='staffpass123',
            is_staff=True
        )
        self.assertTrue(staff_user.is_admin())

    def test_required_fields(self):
        # Test empty email
        user = User(email='', username='test', password='pass123')
        with self.assertRaises(ValidationError):
            user.full_clean()

        # Test empty username
        user = User(email='test@example.com', username='', password='pass123')
        with self.assertRaises(ValidationError):
            user.full_clean()

        # Test password validation
        with self.assertRaises(ValidationError):
            validate_password('')  # Empty password

        with self.assertRaises(ValidationError):
            validate_password('123')  # Too short password

        # Test None values
        user = User(email=None, username='test', password='pass123')
        with self.assertRaises(ValidationError):
            user.full_clean()

        user = User(email='test@example.com', username=None, password='pass123')
        with self.assertRaises(ValidationError):
            user.full_clean() 