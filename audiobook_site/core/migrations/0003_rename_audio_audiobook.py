# Generated by Django 5.2 on 2025-04-12 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_audio_duration'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Audio',
            new_name='AudioBook',
        ),
    ]
