from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.employees.models import Employee
from datetime import date
from ..factories import EmployeeFactory
from apps.authentication.tests.factories import UserFactory

User = get_user_model()

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.employee = EmployeeFactory(created_by=self.user)
        self.user2 = UserFactory()

    def test_create_employee(self):
        employee = EmployeeFactory(created_by=self.user)
        self.assertIsNotNone(employee.pk)
        self.assertIsNotNone(employee.created_by)
        self.assertNotEqual(employee.email, employee.created_by.email)  # Email is now independent

    def test_email_constraints(self):
        # Try to create another employee with same email - should fail
        with self.assertRaises(ValidationError):
            EmployeeFactory(email=self.employee.email)
            
        # Try to create employee with different email - should succeed
        employee2 = EmployeeFactory(created_by=self.user2)
        self.assertIsNotNone(employee2.pk)
        self.assertEqual(employee2.created_by, self.user2)

    def test_required_fields(self):
        # Test without required fields
        required_fields = ['first_name', 'last_name', 'email', 'department', 'position', 'salary', 'hire_date']
        
        for field in required_fields:
            # Create an employee instance but don't save it
            employee = EmployeeFactory.build(created_by=self.user)
            setattr(employee, field, None)
            
            with self.assertRaises(ValidationError):
                employee.full_clean()

    def test_string_representation(self):
        self.assertEqual(str(self.employee), f"{self.employee.first_name} {self.employee.last_name}")

    def test_ordering(self):
        # Create multiple employees
        employee1 = EmployeeFactory(created_by=self.user)
        employee2 = EmployeeFactory(created_by=self.user)
        
        # Check ordering
        employees = list(Employee.objects.all())
        self.assertEqual(employees[0], employee2)  # Should be ordered by -created_at
        self.assertEqual(employees[1], employee1) 