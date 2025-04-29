from rest_framework import serializers
from ..models import LeaveBalance
from apps.employees.serializers import EmployeeSerializer
from .leave_types import LeaveTypeSerializer

class LeaveBalanceSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    leave_type_details = LeaveTypeSerializer(source='leave_type', read_only=True)
    remaining_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = LeaveBalance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')