# Generated by Django 4.0.3 on 2022-05-23 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_alter_schedule_week_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='is_lecture',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='is_practice',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
