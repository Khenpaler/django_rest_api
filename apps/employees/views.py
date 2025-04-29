from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer

# Create your views here.

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_renderer_context(self):
        context = super().get_renderer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        
        # For browsable API, provide raw data
        if self.request.accepted_renderer.format == 'api' or self.request.accepted_renderer.format == 'html':
            context['response'] = self.get_object() if self.action in ['retrieve', 'update', 'partial_update'] else None
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            if request.accepted_renderer.format in ['api', 'html']:
                return Response(serializer.data)
            return Response({
                'message': 'Employee created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Error creating employee',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            if request.accepted_renderer.format in ['api', 'html']:
                return Response(serializer.data)
            return Response({
                'message': 'Employee updated successfully',
                'data': serializer.data
            })
        return Response({
            'message': 'Error updating employee',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.accepted_renderer.format in ['api', 'html']:
            return Response(serializer.data)
        return Response({
            'message': 'Employee retrieved successfully',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            employee_name = str(instance)
            self.perform_destroy(instance)
            return Response({
                'message': f'Employee {employee_name} deleted successfully'
            }, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({
                'message': 'Employee not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': 'Error deleting employee',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if request.accepted_renderer.format in ['api', 'html']:
                return self.get_paginated_response(serializer.data)
            return self.get_paginated_response({
                'message': 'Employees retrieved successfully',
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        if request.accepted_renderer.format in ['api', 'html']:
            return Response(serializer.data)
        return Response({
            'message': 'Employees retrieved successfully',
            'data': serializer.data
        })
