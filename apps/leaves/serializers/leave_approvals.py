from rest_framework import serializers
from ..models import LeaveApproval
from apps.authentication.serializers import UserSerializer

class LeaveApprovalSerializer(serializers.ModelSerializer):
    approver_details = UserSerializer(source='approver', read_only=True)

    class Meta:
        model = LeaveApproval
        fields = ['id', 'leave', 'approver', 'approver_details', 'comments', 'approved_at']
        read_only_fields = ('approved_at', 'approver', 'approver_details') 