# Generated by Django 4.0.3 on 2022-03-15 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.department'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='load',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='one_rate',
            field=models.IntegerField(null=True),
        ),
    ]