from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    department = serializers.CharField(max_length=100)
    position = serializers.CharField(max_length=100)
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    hire_date = serializers.DateField()
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'department', 
                 'position', 'salary', 'hire_date', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'created_by')

    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data) 