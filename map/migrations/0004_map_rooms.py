# Generated by Django 5.1.7 on 2025-03-12 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_alter_map_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='rooms',
            field=models.JSONField(default=dict),
        ),
    ]
