# Generated by Django 4.0.3 on 2022-03-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_first_name_teacher_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='full_name',
            field=models.CharField(max_length=200),
        ),
    ]