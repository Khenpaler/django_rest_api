from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..factories import LeaveFactory, LeaveTypeFactory
from apps.employees.tests.factories import EmployeeFactory
from apps.authentication.tests.factories import UserFactory

class LeaveViewSetTests(APITestCase):
    def setUp(self):
        # Create test data
        self.user = UserFactory(is_staff=True)
        self.employee = EmployeeFactory(user=self.user)
        self.leave_type = LeaveTypeFactory()
        self.leave = LeaveFactory(
            employee=self.employee,
            leave_type=self.leave_type,
            status='pending'  # Set initial status to pending
        )
        
        # URLs
        self.list_url = reverse('leave-list')
        self.detail_url = reverse('leave-detail', kwargs={'pk': self.leave.pk})
        
        # Authenticate
        self.client.force_authenticate(user=self.user)

    def test_list_leaves(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Leaves retrieved successfully')
        self.assertTrue(len(response.data['data']) > 0)

    def test_retrieve_leave(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Leave retrieved successfully')
        self.assertEqual(response.data['data']['id'], self.leave.id)

    def test_create_leave(self):
        data = {
            'employee': self.employee.id,
            'leave_type': self.leave_type.id,
            'start_date': '2024-01-01',
            'end_date': '2024-01-05',
            'reason': 'Test leave request'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Leave created successfully')

    def test_update_leave(self):
        data = {
            'reason': 'Updated reason'
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response doesn't include a message for updates
        self.assertEqual(response.data['reason'], 'Updated reason')

    def test_delete_leave(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('deleted successfully', response.data['message'])

    def test_my_leaves(self):
        url = reverse('leave-my-leaves')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Your leaves retrieved successfully')

    def test_approve_leave(self):
        # Make sure the leave is in pending status
        self.leave.status = 'pending'
        self.leave.save()
        
        url = reverse('leave-approve', kwargs={'pk': self.leave.pk})
        response = self.client.post(url, {'comments': 'Approved for testing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Leave approved successfully')

    def test_reject_leave(self):
        # Make sure the leave is in pending status
        self.leave.status = 'pending'
        self.leave.save()
        
        url = reverse('leave-reject', kwargs={'pk': self.leave.pk})
        response = self.client.post(url, {'comments': 'Rejected for testing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Leave rejected successfully') 