from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.employees.models import Employee
from ..factories import EmployeeFactory
from apps.authentication.tests.factories import UserFactory

class EmployeeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(is_staff=True)  # Create a staff user for testing
        self.client.force_authenticate(user=self.user)
        
        # Create some test employees
        self.employees = [EmployeeFactory() for _ in range(3)]
        self.employee = self.employees[0]
        
        # Create data for a new employee
        self.new_user = UserFactory()
        self.valid_payload = {
            'user': self.new_user.id,
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': self.new_user.email,
            'phone': '555-123-4567',
            'department': 'Marketing',
            'position': 'Marketing Manager',
            'salary': 85000.00,
            'hire_date': '2023-02-01'
        }

    def test_get_all_employees(self):
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), len(self.employees))
        self.assertEqual(response.data['message'], 'Employees retrieved successfully')

    def test_get_single_employee(self):
        response = self.client.get(
            reverse('employee-detail', kwargs={'pk': self.employee.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], self.employee.email)
        self.assertEqual(response.data['message'], 'Employee retrieved successfully')

    def test_create_valid_employee(self):
        response = self.client.post(
            reverse('employee-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Employee created successfully')
        self.assertEqual(Employee.objects.count(), len(self.employees) + 1)

    def test_create_invalid_employee(self):
        invalid_payload = self.valid_payload.copy()
        del invalid_payload['first_name']  # Remove required field
        response = self.client.post(
            reverse('employee-list'),
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Error creating employee')
        self.assertIn('first_name', response.data['errors'])

    def test_update_employee(self):
        update_payload = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '999-999-9999'
        }
        response = self.client.patch(
            reverse('employee-detail', kwargs={'pk': self.employee.pk}),
            data=update_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Employee updated successfully')
        self.assertEqual(response.data['data']['first_name'], update_payload['first_name'])
        self.assertEqual(response.data['data']['last_name'], update_payload['last_name'])
        self.assertEqual(response.data['data']['phone'], update_payload['phone'])

    def test_delete_employee(self):
        response = self.client.delete(
            reverse('employee-detail', kwargs={'pk': self.employee.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('deleted successfully', response.data['message'])
        self.assertEqual(Employee.objects.count(), len(self.employees) - 1)

    def test_unauthorized_access(self):
        # Create a non-staff user
        regular_user = UserFactory(is_staff=False)
        self.client.force_authenticate(user=regular_user)
        
        # Try to access employee list
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to create employee
        response = self.client.post(
            reverse('employee-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to update employee
        response = self.client.patch(
            reverse('employee-detail', kwargs={'pk': self.employee.pk}),
            data={'first_name': 'Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to delete employee
        response = self.client.delete(
            reverse('employee-detail', kwargs={'pk': self.employee.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 