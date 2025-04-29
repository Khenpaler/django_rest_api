from rest_framework import serializers
from ..models import LeaveBalance
from apps.employees.serializers import EmployeeSerializer
from .leave_types import LeaveTypeSerializer
from datetime import datetime

class LeaveBalanceSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    leave_type_details = LeaveTypeSerializer(source='leave_type', read_only=True)
    remaining_days = serializers.IntegerField(read_only=True)
    total_days = serializers.IntegerField(min_value=0)
    used_days = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(min_value=2000, max_value=2100)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LeaveBalance
        fields = ('id', 'employee', 'employee_details', 'leave_type', 'leave_type_details',
                 'total_days', 'used_days', 'remaining_days', 'year', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'used_days', 'remaining_days')

    def validate_total_days(self, value):
        if value < 0:
            raise serializers.ValidationError("Total days cannot be negative")
        return value

    def validate_year(self, value):
        current_year = datetime.now().year
        if value < current_year - 1 or value > current_year + 1:
            raise serializers.ValidationError(f"Year must be between {current_year - 1} and {current_year + 1}")
        return value

    def create(self, validated_data):
        # Set default year to current year if not provided
        if 'year' not in validated_data:
            validated_data['year'] = datetime.now().year
        return super().create(validated_data)