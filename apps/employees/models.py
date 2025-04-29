from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        # Check if another employee exists with the same user
        if self.user:
            existing = Employee.objects.filter(user=self.user).exclude(pk=self.pk).exists()
            if existing:
                raise ValidationError("An employee record already exists for this user.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving
        # Update user's email if employee email changes
        if self.pk and self.user:  # If this is an update and user exists
            if self.user.email != self.email:
                self.user.email = self.email
                self.user.save()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'email']
