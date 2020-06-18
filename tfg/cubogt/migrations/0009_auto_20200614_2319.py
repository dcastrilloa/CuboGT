# Generated by Django 3.0.2 on 2020-06-14 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubogt', '0008_auto_20200612_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partido',
            old_name='juegos_contra',
            new_name='puntos_local',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='juegos_favor',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='puntos_contra',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='puntos_favor',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='sets_contra',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='sets_favor',
        ),
        migrations.AddField(
            model_name='partido',
            name='puntos_visitante',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='partido',
            name='sets_local',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='partido',
            name='sets_visitante',
            field=models.IntegerField(default=0),
        ),
    ]
