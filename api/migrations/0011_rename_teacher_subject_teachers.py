# Generated by Django 4.0.3 on 2022-03-21 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_teacher_excel_column_index'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='teacher',
            new_name='teachers',
        ),
    ]