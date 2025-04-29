from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from ..factories import UserFactory

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_data = {
            'email': self.user.email,
            'username': self.user.username,
            'password': 'testpass123',
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone': self.user.phone,
            'role': self.user.role
        }

    def test_create_user(self):
        user = UserFactory()
        self.assertEqual(user.email, user.email)
        self.assertEqual(user.username, user.username)
        self.assertEqual(user.role, user.role)
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = UserFactory(
            email='admin@example.com',
            username='admin',
            is_staff=True,
            is_superuser=True,
            role='admin'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.role, 'admin')

    def test_email_unique_constraint(self):
        # Create first user
        user1 = UserFactory()
        
        # Try to create user with same email
        with self.assertRaises(IntegrityError):
            UserFactory(email=user1.email)

    def test_is_admin_method(self):
        # Test for regular employee
        user = UserFactory(role='employee')
        self.assertFalse(user.is_admin())

        # Test for admin role
        admin_user = UserFactory(role='admin')
        self.assertTrue(admin_user.is_admin())

        # Test for staff user
        staff_user = UserFactory(is_staff=True)
        self.assertTrue(staff_user.is_admin())

    def test_required_fields(self):
        # Test empty email
        user = UserFactory.build(email='')
        with self.assertRaises(ValidationError):
            user.full_clean()

        # Test empty username
        user = UserFactory.build(username='')
        with self.assertRaises(ValidationError):
            user.full_clean()

        # Test password validation
        with self.assertRaises(ValidationError):
            validate_password('')  # Empty password

        with self.assertRaises(ValidationError):
            validate_password('123')  # Too short password

        # Test None values
        user = UserFactory.build(email=None)
        with self.assertRaises(ValidationError):
            user.full_clean()

        user = UserFactory.build(username=None)
        with self.assertRaises(ValidationError):
            user.full_clean() 