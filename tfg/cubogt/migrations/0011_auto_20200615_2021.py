# Generated by Django 3.0.2 on 2020-06-15 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cubogt', '0010_auto_20200615_1917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partido',
            old_name='juego_local',
            new_name='juegos_local',
        ),
        migrations.RenameField(
            model_name='partido',
            old_name='juego_visitante',
            new_name='juegos_visitante',
        ),
    ]
