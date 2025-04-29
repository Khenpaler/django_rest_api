from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import LeaveBalance
from ..serializers import LeaveBalanceSerializer

class LeaveBalanceViewSet(viewsets.ModelViewSet):
    queryset = LeaveBalance.objects.all()  # Add default queryset
    serializer_class = LeaveBalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return LeaveBalance.objects.filter(employee__user=self.request.user)
        return LeaveBalance.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'message': 'Leave balance created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Error creating leave balance',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response({
                    'message': 'Leave balance updated successfully',
                    'data': serializer.data
                })
            return Response({
                'message': 'Error updating leave balance',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': 'Error updating leave balance',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            employee_name = str(instance.employee)
            leave_type = str(instance.leave_type)
            self.perform_destroy(instance)
            return Response({
                'message': f'Leave balance for {employee_name} ({leave_type}) deleted successfully'
            }, status=status.HTTP_200_OK)
        except LeaveBalance.DoesNotExist:
            return Response({
                'message': 'Leave balance not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': 'Error deleting leave balance',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'message': 'Leave balance retrieved successfully',
                'data': serializer.data
            })
        except LeaveBalance.DoesNotExist:
            return Response({
                'message': 'Leave balance not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Leave balances retrieved successfully',
            'data': serializer.data
        })
