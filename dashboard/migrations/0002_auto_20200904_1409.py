# Generated by Django 3.1 on 2020-09-04 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Story',
            new_name='Quiz',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='story',
            new_name='quiz',
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='story_text',
            new_name='quiz_text',
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='story_title',
            new_name='quiz_title',
        ),
    ]
