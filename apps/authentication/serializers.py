from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name', 'phone', 'role')
        read_only_fields = ('role',)  # Role can't be set during registration

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        # Check if this is the first user being created
        is_first_user = not User.objects.exists()
        
        user = User.objects.create_user(**validated_data)
        
        # If this is the first user, make them an admin
        if is_first_user:
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.save()
        
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone', 'role', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at') 