from rest_framework import serializers
from ..models import LeaveApproval

class LeaveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApproval
        fields = '__all__'
        read_only_fields = ('approved_at',) 