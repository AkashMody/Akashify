# Generated by Django 5.0.6 on 2024-05-13 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaPlay', '0012_alter_listener_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
