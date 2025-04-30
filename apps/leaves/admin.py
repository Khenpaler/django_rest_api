from django.contrib import admin
from .models import LeaveType, Leave, LeaveApproval

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_days', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'leave_type', 'start_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'reason')
    date_hierarchy = 'start_date'

@admin.register(LeaveApproval)
class LeaveApprovalAdmin(admin.ModelAdmin):
    list_display = ('leave', 'approver', 'approved_at')
    search_fields = ('leave__employee__first_name', 'leave__employee__last_name', 'comments')
