# Generated by Django 4.0.3 on 2022-05-30 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_schedule_group_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='group_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='is_lab',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='teacher_name',
            field=models.CharField(max_length=200),
        ),
    ]
