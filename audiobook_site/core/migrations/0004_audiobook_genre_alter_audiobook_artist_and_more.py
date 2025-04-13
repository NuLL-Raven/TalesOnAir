# Generated by Django 5.2 on 2025-04-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_audio_audiobook'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiobook',
            name='genre',
            field=models.CharField(choices=[('fiction', 'Fiction'), ('nonfiction', 'Non-fiction'), ('mystery', 'Mystery'), ('fantasy', 'Fantasy'), ('sci-fi', 'Sci-Fi'), ('romance', 'Romance'), ('history', 'History')], default='fiction', max_length=50),
        ),
        migrations.AlterField(
            model_name='audiobook',
            name='artist',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='audiobook',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
