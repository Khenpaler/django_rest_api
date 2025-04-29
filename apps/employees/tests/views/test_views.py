from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
from apps.employees.models import Employee

User = get_user_model()

class EmployeeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        # Create token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.employee_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'department': 'Engineering',
            'position': 'Software Engineer',
            'salary': 75000.00,
            'hire_date': '2023-01-01'
        }

    def test_create_employee(self):
        response = self.client.post('/api/employees/', self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(email=self.employee_data['email']).exists())
        self.assertEqual(response.data['message'], 'Employee created successfully')

    def test_create_employee_duplicate(self):
        # Create first employee
        self.client.post('/api/employees/', self.employee_data)
        
        # Try to create another employee for the same user
        response = self.client.post('/api/employees/', self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'User already has an employee record')

    def test_list_employees(self):
        # Create an employee
        employee = Employee.objects.create(
            user=self.user,
            **self.employee_data
        )
        
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Employees retrieved successfully')
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['email'], employee.email)

    def test_retrieve_employee(self):
        # Create an employee
        employee = Employee.objects.create(
            user=self.user,
            **self.employee_data
        )
        
        response = self.client.get(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Employee retrieved successfully')
        self.assertEqual(response.data['data']['email'], employee.email)

    def test_update_employee(self):
        # Create an employee
        employee = Employee.objects.create(
            user=self.user,
            **self.employee_data
        )
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '9999999999',
            'department': 'Updated Department',
            'position': 'Updated Position',
            'salary': 90000.00
        }
        
        response = self.client.patch(f'/api/employees/{employee.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Employee updated successfully')
        
        # Refresh employee from database
        employee.refresh_from_db()
        self.assertEqual(employee.first_name, update_data['first_name'])
        self.assertEqual(employee.last_name, update_data['last_name'])
        self.assertEqual(employee.phone, update_data['phone'])
        self.assertEqual(employee.department, update_data['department'])
        self.assertEqual(employee.position, update_data['position'])
        self.assertEqual(float(employee.salary), float(update_data['salary']))

    def test_delete_employee(self):
        # Create an employee
        employee = Employee.objects.create(
            user=self.user,
            **self.employee_data
        )
        
        response = self.client.delete(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'Employee {employee} deleted successfully')
        self.assertFalse(Employee.objects.filter(id=employee.id).exists())

    def test_unauthorized_access(self):
        # Remove authentication
        self.client.credentials()
        
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 