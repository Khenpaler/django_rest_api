from rest_framework import serializers
from ..models import LeaveApproval
from apps.authentication.serializers import UserSerializer

class LeaveApprovalSerializer(serializers.ModelSerializer):
    approver_details = UserSerializer(source='approver', read_only=True)
    comments = serializers.CharField(max_length=500, required=False, allow_blank=True)
    approved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LeaveApproval
        fields = ['id', 'leave', 'approver', 'approver_details', 'comments', 'approved_at']
        read_only_fields = ('approved_at', 'approver_details', 'approver')

    def create(self, validated_data):
        validated_data['approver'] = self.context['request'].user
        return super().create(validated_data) 