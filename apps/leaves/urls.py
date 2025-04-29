from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveViewSet, LeaveBalanceViewSet, LeaveApprovalViewSet

router = DefaultRouter()
router.register(r'leave-types', LeaveTypeViewSet)
router.register(r'leaves', LeaveViewSet)
router.register(r'leave-balances', LeaveBalanceViewSet)
router.register(r'leave-approvals', LeaveApprovalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
