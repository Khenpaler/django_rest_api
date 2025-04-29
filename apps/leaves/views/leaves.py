from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from ..models import Leave, LeaveApproval
from ..serializers import LeaveSerializer
import logging

logger = logging.getLogger(__name__)

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = Leave.objects.all()
            if not self.request.user.is_staff:
                # Get the employee associated with the current user
                try:
                    employee = self.request.user.employee
                    queryset = queryset.filter(employee=employee)
                except ObjectDoesNotExist:
                    logger.error(f"No employee record found for user {self.request.user.id}")
                    return Leave.objects.none()
            return queryset.select_related('employee', 'leave_type')
        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}")
            return Leave.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'message': 'Leaves retrieved successfully',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in list view: {str(e)}")
            return Response({
                'message': 'Error retrieving leaves',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            # If user is not staff, set employee to current user's employee
            if not request.user.is_staff:
                try:
                    employee = request.user.employee
                    request.data['employee'] = employee.id
                except ObjectDoesNotExist:
                    return Response({
                        'message': 'No employee record found for current user',
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({
                    'message': 'Leave created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Error creating leave',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in create: {str(e)}")
            return Response({
                'message': 'Error creating leave',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def my_leaves(self, request):
        try:
            employee = request.user.employee
            leaves = self.get_queryset().filter(employee=employee)
            serializer = self.get_serializer(leaves, many=True)
            return Response({
                'message': 'Your leaves retrieved successfully',
                'data': serializer.data
            })
        except ObjectDoesNotExist:
            return Response({
                'message': 'No employee record found for current user',
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in my_leaves: {str(e)}")
            return Response({
                'message': 'Error retrieving leaves',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            leave = self.get_object()
            if leave.status != 'pending':
                return Response({
                    'message': 'Leave is not in pending status'
                }, status=status.HTTP_400_BAD_REQUEST)

            leave.status = 'approved'
            leave.save()

            LeaveApproval.objects.create(
                leave=leave,
                approver=request.user,
                comments=request.data.get('comments', '')
            )

            return Response({
                'message': 'Leave approved successfully',
                'data': self.get_serializer(leave).data
            })
        except Exception as e:
            logger.error(f"Error in approve: {str(e)}")
            return Response({
                'message': 'Error approving leave',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        try:
            leave = self.get_object()
            if leave.status != 'pending':
                return Response({
                    'message': 'Leave is not in pending status'
                }, status=status.HTTP_400_BAD_REQUEST)

            leave.status = 'rejected'
            leave.save()

            LeaveApproval.objects.create(
                leave=leave,
                approver=request.user,
                comments=request.data.get('comments', '')
            )

            return Response({
                'message': 'Leave rejected successfully',
                'data': self.get_serializer(leave).data
            })
        except Exception as e:
            logger.error(f"Error in reject: {str(e)}")
            return Response({
                'message': 'Error rejecting leave',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
