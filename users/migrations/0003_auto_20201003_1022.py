# Generated by Django 3.1 on 2020-10-03 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200902_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='teacher',
            field=models.BooleanField(default=False, help_text='check if you are a teacher. Only teachers can create quizzes'),
        ),
    ]
