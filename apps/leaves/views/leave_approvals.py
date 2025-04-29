from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
            if not self.request.user.is_staff:
                # Regular users can only see their own leave approvals
                queryset = queryset.filter(leave__employee__user=self.request.user)
            return queryset.select_related('leave', 'approver')
        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}")
            return LeaveApproval.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            # Set the approver to the current user
            request.data['approver'] = request.user.id
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
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
            # Only allow updating comments
            if 'comments' in request.data:
                serializer = self.get_serializer(instance, data={'comments': request.data['comments']}, partial=True)
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
            # Check if the user is the approver
            if instance.approver != request.user and not request.user.is_staff:
                return Response({
                    'message': 'You do not have permission to delete this approval'
                }, status=status.HTTP_403_FORBIDDEN)
                
            self.perform_destroy(instance)
            return Response({
                'message': 'Leave approval deleted successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in destroy: {str(e)}")
            return Response({
                'message': 'Error deleting leave approval',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 