# Generated by Django 3.0.2 on 2020-06-12 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubogt', '0007_auto_20200611_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fase',
            options={'ordering': ['numero_activacion', 'nombre']},
        ),
        migrations.AddField(
            model_name='fase',
            name='numero_activacion',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
