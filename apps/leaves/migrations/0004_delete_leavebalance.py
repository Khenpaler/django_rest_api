# Generated by Django 5.2 on 2025-04-30 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0003_remove_leavetype_is_paid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LeaveBalance',
        ),
    ]
