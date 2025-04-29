from rest_framework import serializers
from ..models import Leave
from apps.employees.serializers import EmployeeSerializer
from .leave_types import LeaveTypeSerializer

class LeaveSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    leave_type_details = LeaveTypeSerializer(source='leave_type', read_only=True)
    duration = serializers.IntegerField(read_only=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    reason = serializers.CharField(max_length=500)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Leave
        fields = ('id', 'employee', 'employee_details', 'leave_type', 'leave_type_details', 
                 'start_date', 'end_date', 'reason', 'status', 'duration', 
                 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'status', 'duration')

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

    def create(self, validated_data):
        validated_data['status'] = 'pending'
        return super().create(validated_data) 