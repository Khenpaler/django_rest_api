from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'position', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'department')
    list_filter = ('department', 'position', 'hire_date')
