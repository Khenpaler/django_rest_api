from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ..models import LeaveApproval
from ..serializers import LeaveApprovalSerializer
import logging

logger = logging.getLogger(__name__)

class LeaveApprovalViewSet(viewsets.ModelViewSet):
    queryset = LeaveApproval.objects.all()
    serializer_class = LeaveApprovalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = LeaveApproval.objects.all()
            if not self.request.user.is_admin():
                # Regular users can only see their own leave approvals
                queryset = queryset.filter(leave__employee__user=self.request.user)
            return queryset.select_related('leave', 'approver', 'leave__employee')
        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}")
            return LeaveApproval.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            # Only admins can create approvals
            if not request.user.is_admin():
                return Response({
                    'message': 'Only admins can approve leaves'
                }, status=status.HTTP_403_FORBIDDEN)

            data = {
                'leave': request.data.get('leave'),
                'comments': request.data.get('comments', ''),
                'approver': request.user.id
            }
            
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                # Check if leave is already approved
                leave = serializer.validated_data['leave']
                if leave.status != 'pending':
                    return Response({
                        'message': f'Leave is already {leave.status}'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Check if leave already has an approval
                if LeaveApproval.objects.filter(leave=leave).exists():
                    return Response({
                        'message': 'Leave already has an approval'
                    }, status=status.HTTP_400_BAD_REQUEST)

                self.perform_create(serializer)
                
                # Update leave status
                leave.status = 'approved'
                leave.save()

                return Response({
                    'message': 'Leave approval created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Error creating leave approval',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in create: {str(e)}")
            return Response({
                'message': 'Error creating leave approval',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Only admin can update approvals
            if not request.user.is_admin():
                return Response({
                    'message': 'Only admins can update approvals'
                }, status=status.HTTP_403_FORBIDDEN)

            # Only allow updating comments
            if 'comments' in request.data:
                data = {'comments': request.data['comments']}
                serializer = self.get_serializer(instance, data=data, partial=True)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response({
                        'message': 'Leave approval updated successfully',
                        'data': serializer.data
                    })
            return Response({
                'message': 'Only comments can be updated',
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in update: {str(e)}")
            return Response({
                'message': 'Error updating leave approval',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Only admin can delete approvals
            if not request.user.is_admin():
                return Response({
                    'message': 'Only admins can delete approvals'
                }, status=status.HTTP_403_FORBIDDEN)

            # Store approval info before deletion
            approval_info = f"Approval for {instance.leave}"
            
            # Update leave status back to pending
            leave = instance.leave
            leave.status = 'pending'
            leave.save()
            
            self.perform_destroy(instance)
            return Response({
                'message': f'{approval_info} deleted successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in destroy: {str(e)}")
            return Response({
                'message': 'Error deleting leave approval',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Check if user has permission to view this approval
            if not request.user.is_admin() and instance.leave.employee.user != request.user:
                return Response({
                    'message': 'You do not have permission to view this approval'
                }, status=status.HTTP_403_FORBIDDEN)
                
            serializer = self.get_serializer(instance)
            return Response({
                'message': 'Leave approval retrieved successfully',
                'data': serializer.data
            })
        except LeaveApproval.DoesNotExist:
            return Response({
                'message': 'Leave approval not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in retrieve: {str(e)}")
            return Response({
                'message': 'Error retrieving leave approval',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 