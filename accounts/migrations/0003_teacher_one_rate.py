# Generated by Django 4.0.3 on 2022-05-17 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='one_rate',
            field=models.IntegerField(null=True),
        ),
    ]
