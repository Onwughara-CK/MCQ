# Generated by Django 3.1 on 2020-10-09 06:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_auto_20201008_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]