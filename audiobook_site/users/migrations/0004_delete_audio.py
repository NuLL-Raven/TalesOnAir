# Generated by Django 5.2 on 2025-04-12 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_audio'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Audio',
        ),
    ]
