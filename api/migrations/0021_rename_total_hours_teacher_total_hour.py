# Generated by Django 4.0.3 on 2022-03-23 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_teacher_total_hours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='total_hours',
            new_name='total_hour',
        ),
    ]
