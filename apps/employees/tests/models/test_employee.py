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
        self.employee = EmployeeFactory()
        self.user2 = UserFactory()

    def test_create_employee(self):
        employee = EmployeeFactory()
        self.assertIsNotNone(employee.pk)
        self.assertIsNotNone(employee.user)
        self.assertEqual(employee.email, employee.user.email)

    def test_user_and_email_constraints(self):
        # Try to create another employee with same user - should fail
        with self.assertRaises(ValidationError):
            EmployeeFactory(user=self.employee.user)
            
        # Try to create employee with different user - should succeed
        employee2 = EmployeeFactory(user=self.user2)
        self.assertIsNotNone(employee2.pk)
        self.assertEqual(employee2.user, self.user2)

    def test_required_fields(self):
        # Test without required fields
        required_fields = ['first_name', 'last_name', 'email', 'department', 'position', 'salary', 'hire_date']
        
        for field in required_fields:
            # Create an employee instance but don't save it
            employee = EmployeeFactory.build()
            setattr(employee, field, None)
            
            # Save the user first if it exists (to avoid related object validation error)
            if employee.user and not employee.user.pk:
                employee.user.save()
                
            with self.assertRaises(ValidationError):
                employee.full_clean()

    def test_email_update_syncs_with_user(self):
        # Update employee email
        new_email = 'new.email@example.com'
        self.employee.email = new_email
        self.employee.save()
        
        # Check if user email was updated
        self.employee.user.refresh_from_db()
        self.assertEqual(self.employee.user.email, new_email)

    def test_string_representation(self):
        self.assertEqual(str(self.employee), f"{self.employee.first_name} {self.employee.last_name}")

    def test_ordering(self):
        # Create multiple employees
        employee1 = EmployeeFactory()
        employee2 = EmployeeFactory()
        
        # Check ordering
        employees = list(Employee.objects.all())
        self.assertEqual(employees[0], employee2)  # Should be ordered by -created_at
        self.assertEqual(employees[1], employee1) 