# Generated by Django 4.1.5 on 2023-01-06 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='song',
            field=models.ManyToManyField(blank=True, related_name='playlists', to='playlists.song'),
        ),
    ]