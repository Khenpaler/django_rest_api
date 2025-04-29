from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveViewSet, LeaveBalanceViewSet

router = DefaultRouter()
router.register(r'leave-types', LeaveTypeViewSet)
router.register(r'leaves', LeaveViewSet)
router.register(r'leave-balances', LeaveBalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
