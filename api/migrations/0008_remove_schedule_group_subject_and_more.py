# Generated by Django 4.0.3 on 2022-05-30 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_schedule_is_lecture_alter_schedule_is_practice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='group_subject',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='teacher',
        ),
        migrations.AddField(
            model_name='schedule',
            name='group_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='is_lab',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='subject_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='teacher_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]