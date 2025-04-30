from django.http import HttpResponseForbidden
from django.urls import resolve
from functools import wraps
from rest_framework.permissions import BasePermission

class EmployeeRolePermission(BasePermission):
    """
    Custom permission class for role-based access control.
    """
    def has_permission(self, request, view):
        # Admin users can access everything
        if request.user.is_authenticated and (request.user.is_admin() or request.user.is_staff):
            return True

        # Allow all authenticated users to view leave types and leave approvals
        if view.action in ['list', 'retrieve'] and view.__class__.__name__ in ['LeaveTypeViewSet', 'LeaveApprovalViewSet']:
            return request.user.is_authenticated

        # For LeaveViewSet, employees can perform all actions on their own leaves
        if view.__class__.__name__ == 'LeaveViewSet':
            if view.action in ['create', 'list', 'retrieve', 'update', 'partial_update']:
                return request.user.is_authenticated and hasattr(request.user, 'employee_profile')
            return False

        return False

    def has_object_permission(self, request, view, obj):
        # Admin users can access everything
        if request.user.is_authenticated and (request.user.is_admin() or request.user.is_staff):
            return True

        # For leaves, employees can only access their own leaves
        if view.__class__.__name__ == 'LeaveViewSet':
            return obj.employee.user == request.user

        return False 