from rest_framework import serializers
from ..models import Leave
from apps.employees.serializers import EmployeeSerializer
from .leave_types import LeaveTypeSerializer

class LeaveSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    leave_type_details = LeaveTypeSerializer(source='leave_type', read_only=True)
    duration = serializers.IntegerField(read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'status') 