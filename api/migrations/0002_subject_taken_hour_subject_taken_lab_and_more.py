# Generated by Django 4.0.3 on 2022-05-20 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='taken_hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='taken_lab',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='taken_lectures',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='taken_office',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='taken_practice',
            field=models.IntegerField(default=0),
        ),
    ]