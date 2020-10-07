# Generated by Django 3.1 on 2020-10-06 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.PositiveIntegerField(default=0)),
                ('time_spent', models.DurationField(default=0)),
                ('failed', models.IntegerField(default=0)),
                ('passed', models.IntegerField(default=0)),
                ('no_of_questions', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
