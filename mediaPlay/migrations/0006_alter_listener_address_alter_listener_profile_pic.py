# Generated by Django 5.0.4 on 2024-05-07 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaPlay', '0005_listener_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listener',
            name='address',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='listener',
            name='profile_pic',
            field=models.ImageField(default='user_profile_pic/guest.jpg', upload_to='user_profile_pic'),
        ),
    ]
