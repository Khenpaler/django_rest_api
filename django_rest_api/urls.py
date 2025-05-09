"""
URL configuration for django_rest_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import RedirectView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter
from apps.leaves.views import LeaveTypeViewSet, LeaveViewSet, LeaveApprovalViewSet


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root view that provides links to all main endpoints.
    This serves as the entry point and documentation for the API.
    """
    return Response({
        # Employee management endpoints
        'employees': reverse('employee-list', request=request, format=format),
        
        # Leave management endpoints
        'leave_types': reverse('leavetype-list', request=request, format=format),
        'leaves': reverse('leave-list', request=request, format=format),
        'leave_approvals': reverse('leaveapproval-list', request=request, format=format),
    })


router = DefaultRouter()
router.register(r'leave_types', LeaveTypeViewSet)
router.register(r'leaves', LeaveViewSet)
router.register(r'leave_approvals', LeaveApprovalViewSet)

urlpatterns = [
    # Redirect root to API documentation
    path('', RedirectView.as_view(url='api/', permanent=False)),
    
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API root and documentation
    path('api/', api_root, name='api-root'),
    
    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('apps.authentication.urls')),
    
    # Core application endpoints
    path('api/', include('apps.employees.urls')),
    path('api/', include(router.urls)),
    
    # Django REST Framework authentication views
    path('api-auth/', include('rest_framework.urls')),
]
