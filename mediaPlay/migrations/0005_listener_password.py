# Generated by Django 5.0.4 on 2024-05-06 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaPlay', '0004_remove_listener_name_listener_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listener',
            name='password',
            field=models.CharField(default='', max_length=16),
        ),
    ]
