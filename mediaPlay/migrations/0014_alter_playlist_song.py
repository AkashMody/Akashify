# Generated by Django 5.0.6 on 2024-05-13 05:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaPlay', '0013_alter_payment_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mediaPlay.song'),
        ),
    ]
