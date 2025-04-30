from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_employees',
        help_text="The user who created this employee record",
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
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

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Create user account if it doesn't exist
        if not self.user:
            User = get_user_model()
            username = slugify(f"{self.first_name}{self.last_name}")
            password = f"{self.last_name.lower()}123"
            
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=self.email,
                password=password,
                first_name=self.first_name,
                last_name=self.last_name,
                phone=self.phone,
                role='employee'
            )
            self.user = user
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
