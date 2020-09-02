# Generated by Django 3.1 on 2020-09-02 21:49

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
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_title', models.CharField(max_length=100)),
                ('story_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=250)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='dashboard.story')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=250)),
                ('mark', models.CharField(choices=[('right', 'Right'), ('wrong', 'Wrong')], default='wrong', max_length=5)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='dashboard.question')),
                ('users', models.ManyToManyField(related_name='choices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
