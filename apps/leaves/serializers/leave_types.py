from rest_framework import serializers
from ..models import LeaveType

class LeaveTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    max_days = serializers.IntegerField(min_value=0)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LeaveType
        fields = ('id', 'name', 'description', 'max_days', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate_max_days(self, value):
        if value < 0:
            raise serializers.ValidationError("Maximum days cannot be negative")
        return value 