# Generated by Django 5.0.4 on 2024-05-12 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaPlay', '0010_alter_playlist_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False)),
                ('membership', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('pdate', models.DateTimeField(auto_now_add=True)),
                ('listener', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mediaPlay.listener')),
            ],
        ),
    ]
