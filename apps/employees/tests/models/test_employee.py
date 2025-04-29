from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.employees.models import Employee
from datetime import date

User = get_user_model()

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='test1@example.com',
            username='testuser1',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            email='test2@example.com',
            username='testuser2',
            password='testpass123'
        )
        
        self.employee_data = {
            'user': self.user1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'department': 'Engineering',
            'position': 'Software Engineer',
            'salary': 75000.00,
            'hire_date': date(2023, 1, 1)
        }

    def test_create_employee(self):
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(employee.first_name, self.employee_data['first_name'])
        self.assertEqual(employee.last_name, self.employee_data['last_name'])
        self.assertEqual(employee.email, self.employee_data['email'])
        self.assertEqual(employee.department, self.employee_data['department'])
        self.assertEqual(employee.position, self.employee_data['position'])
        self.assertEqual(employee.salary, self.employee_data['salary'])
        self.assertEqual(employee.hire_date, self.employee_data['hire_date'])
        self.assertEqual(employee.user, self.user1)

    def test_user_and_email_constraints(self):
        # Create first employee
        employee1 = Employee.objects.create(**self.employee_data)
        
        # Try to create another employee with same user - should fail
        duplicate_data = self.employee_data.copy()
        duplicate_data['email'] = 'different@example.com'
        with self.assertRaises(ValidationError):
            Employee.objects.create(**duplicate_data)
            
        # Try to create employee with same email but different user - should succeed
        duplicate_data = self.employee_data.copy()
        duplicate_data['user'] = self.user2
        duplicate_data['email'] = 'different@example.com'  # Different email for different user
        try:
            Employee.objects.create(**duplicate_data)
        except ValidationError:
            self.fail("Should not raise ValidationError when creating employee with different user and email")

    def test_required_fields(self):
        # Test without required fields
        required_fields = ['first_name', 'last_name', 'email', 'department', 'position', 'salary', 'hire_date']
        
        for field in required_fields:
            data = self.employee_data.copy()
            del data[field]
            employee = Employee(**data)
            with self.assertRaises(ValidationError):
                employee.full_clean()

    def test_email_update_syncs_with_user(self):
        # Create employee
        employee = Employee.objects.create(**self.employee_data)
        
        # Update employee email
        new_email = 'new.email@example.com'
        employee.email = new_email
        employee.save()
        
        # Check if user email was updated
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, new_email)

    def test_string_representation(self):
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(str(employee), f"{self.employee_data['first_name']} {self.employee_data['last_name']}")

    def test_ordering(self):
        # Create multiple employees with different users
        employee1 = Employee.objects.create(**self.employee_data)
        
        employee2_data = self.employee_data.copy()
        employee2_data['user'] = self.user2
        employee2_data['email'] = 'employee2@example.com'
        employee2 = Employee.objects.create(**employee2_data)
        
        # Check ordering
        employees = Employee.objects.all()
        self.assertEqual(list(employees), [employee2, employee1])  # Should be ordered by -created_at 
        self.assertEqual(list(employees), [employee2, employee1])  # Should be ordered by -created_at 

    def test_user_and_email_constraints(self):
        # Create first employee
        employee1 = Employee.objects.create(**self.employee_data)
        
        # Try to create another employee with same user - should fail
        duplicate_data = self.employee_data.copy()
        duplicate_data['email'] = 'different@example.com'
        with self.assertRaises(ValidationError):
            Employee.objects.create(**duplicate_data)
            
        # Try to create employee with same email but different user - should succeed
        duplicate_data = self.employee_data.copy()
        duplicate_data['user'] = self.user2
        duplicate_data['email'] = 'different@example.com'  # Different email for different user
        try:
            Employee.objects.create(**duplicate_data)
        except ValidationError:
            self.fail("Should not raise ValidationError when creating employee with different user and email") 