from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer

User = get_user_model()

class EmployeeSerializerTest(TestCase):
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
        
        self.employee = Employee.objects.create(
            user=self.user1,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            department='Engineering',
            position='Software Engineer',
            salary=75000.00,
            hire_date=date(2023, 1, 1)
        )

        self.valid_data = {
            'user': self.user2.id,  # Use different user for validation tests
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '0987654321',
            'department': 'Marketing',
            'position': 'Marketing Manager',
            'salary': 85000.00,
            'hire_date': '2023-02-01'
        }

    def test_serialization(self):
        serializer = EmployeeSerializer(self.employee)
        data = serializer.data
        
        self.assertEqual(data['first_name'], self.employee.first_name)
        self.assertEqual(data['last_name'], self.employee.last_name)
        self.assertEqual(data['email'], self.employee.email)
        self.assertEqual(data['phone'], self.employee.phone)
        self.assertEqual(data['department'], self.employee.department)
        self.assertEqual(data['position'], self.employee.position)
        self.assertEqual(float(data['salary']), float(self.employee.salary))
        self.assertEqual(data['hire_date'], self.employee.hire_date.strftime('%Y-%m-%d'))
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_deserialization(self):
        serializer = EmployeeSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        employee = serializer.save()
        self.assertEqual(employee.first_name, self.valid_data['first_name'])
        self.assertEqual(employee.last_name, self.valid_data['last_name'])
        self.assertEqual(employee.email, self.valid_data['email'])
        self.assertEqual(employee.phone, self.valid_data['phone'])
        self.assertEqual(employee.department, self.valid_data['department'])
        self.assertEqual(employee.position, self.valid_data['position'])
        self.assertEqual(float(employee.salary), float(self.valid_data['salary']))
        self.assertEqual(employee.hire_date.strftime('%Y-%m-%d'), self.valid_data['hire_date'])

    def test_update(self):
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '9999999999',
            'department': 'Updated Department',
            'position': 'Updated Position',
            'salary': 90000.00
        }
        
        serializer = EmployeeSerializer(self.employee, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_employee = serializer.save()
        self.assertEqual(updated_employee.first_name, update_data['first_name'])
        self.assertEqual(updated_employee.last_name, update_data['last_name'])
        self.assertEqual(updated_employee.phone, update_data['phone'])
        self.assertEqual(updated_employee.department, update_data['department'])
        self.assertEqual(updated_employee.position, update_data['position'])
        self.assertEqual(float(updated_employee.salary), float(update_data['salary']))

    def test_validation(self):
        # Test invalid email
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = EmployeeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

        # Test negative salary
        invalid_data = self.valid_data.copy()
        invalid_data['salary'] = -1000.00
        serializer = EmployeeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('salary', serializer.errors)

        # Test missing required field
        invalid_data = self.valid_data.copy()
        del invalid_data['first_name']
        serializer = EmployeeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors) 