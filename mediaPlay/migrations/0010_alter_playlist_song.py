# Generated by Django 5.0.4 on 2024-05-08 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaPlay', '0009_alter_playlist_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='song',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mediaPlay.song'),
        ),
    ]
