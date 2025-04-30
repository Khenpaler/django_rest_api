from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import LeaveType
from ..serializers import LeaveTypeSerializer
from ..middleware import EmployeeRolePermission
import logging

logger = logging.getLogger(__name__)

class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated, EmployeeRolePermission]

    def get_renderer_context(self):
        context = super().get_renderer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        
        # For browsable API, provide raw data
        if self.request.accepted_renderer.format == 'api' or self.request.accepted_renderer.format == 'html':
            context['response'] = self.get_object() if self.action in ['retrieve', 'update', 'partial_update'] else None
        return context

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                if request.accepted_renderer.format in ['api', 'html']:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({
                    'message': 'Leave type created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Error creating leave type',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in create: {str(e)}")
            return Response({
                'message': 'Error creating leave type',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
            if serializer.is_valid():
                self.perform_update(serializer)
                if request.accepted_renderer.format in ['api', 'html']:
                    return Response(serializer.data)
                return Response({
                    'message': 'Leave type updated successfully',
                    'data': serializer.data
                })
            return Response({
                'message': 'Error updating leave type',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in update: {str(e)}")
            return Response({
                'message': 'Error updating leave type',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            leave_type_name = str(instance)
            self.perform_destroy(instance)
            return Response({
                'message': f'Leave type {leave_type_name} deleted successfully'
            }, status=status.HTTP_200_OK)
        except LeaveType.DoesNotExist:
            return Response({
                'message': 'Leave type not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': 'Error deleting leave type',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            if request.accepted_renderer.format in ['api', 'html']:
                return Response(serializer.data)
            return Response({
                'message': 'Leave type retrieved successfully',
                'data': serializer.data
            })
        except LeaveType.DoesNotExist:
            return Response({
                'message': 'Leave type not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in retrieve: {str(e)}")
            return Response({
                'message': 'Error retrieving leave type',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            if request.accepted_renderer.format in ['api', 'html']:
                return Response(serializer.data)
            return Response({
                'message': 'Leave types retrieved successfully',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in list: {str(e)}")
            return Response({
                'message': 'Error retrieving leave types',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
