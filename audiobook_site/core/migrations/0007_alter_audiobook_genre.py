# Generated by Django 5.2 on 2025-04-12 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_audiobook_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiobook',
            name='genre',
            field=models.CharField(choices=[('fiction', 'Fiction'), ('nonfiction', 'Non-fiction'), ('mystery', 'Mystery'), ('fantasy', 'Fantasy'), ('sci-fi', 'Sci-Fi'), ('romance', 'Romance'), ('history', 'History')], default='', max_length=50),
        ),
    ]
