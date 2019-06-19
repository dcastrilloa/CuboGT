# Generated by Django 2.2.2 on 2019-06-19 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default=None, max_length=50)),
                ('numero_campo', models.IntegerField()),
                ('cubo', models.GenericIPAddressField(blank=True, default=None, null=True)),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fase_numero', models.IntegerField()),
                ('nombre', models.CharField(blank=True, max_length=100)),
                ('numero_equipos', models.IntegerField()),
                ('numero_grupos', models.IntegerField()),
                ('numero_sets', models.IntegerField()),
                ('numero_puntos', models.IntegerField()),
                ('puntos_maximos', models.IntegerField(default=None, null=True)),
                ('tipo_fase', models.IntegerField()),
                ('doble_partid', models.BooleanField()),
                ('cambio_de_campo', models.BooleanField()),
                ('cambio_a_los', models.IntegerField(default=None)),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default=None, max_length=50)),
                ('numero_grupo', models.IntegerField()),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
                ('fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Fase')),
            ],
            options={
                'ordering': ['numero_grupo'],
            },
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado_local', models.IntegerField()),
                ('resultado_visitante', models.IntegerField()),
                ('jornada', models.IntegerField()),
                ('esta_terminado', models.BooleanField()),
                ('es_eliminatoria', models.BooleanField()),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Campo')),
                ('equipo_local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_equipo', to='cubogt.Equipo')),
                ('equipo_visitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitante_equipo', to='cubogt.Equipo')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('estado', models.IntegerField()),
                ('fecha', models.DateField()),
                ('tipo_torneo', models.IntegerField()),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
                ('deporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Deporte')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SetVoleibol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_set', models.IntegerField()),
                ('puntos_local', models.IntegerField()),
                ('puntos_visitante', models.IntegerField()),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Partido')),
            ],
            options={
                'ordering': ['numero_set'],
            },
        ),
        migrations.AddField(
            model_name='fase',
            name='torneo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Torneo'),
        ),
        migrations.AddField(
            model_name='equipo',
            name='torneo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Torneo'),
        ),
        migrations.CreateModel(
            name='Clasificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partidos_jugados', models.IntegerField(default=0)),
                ('partidos_ganados', models.IntegerField(default=0)),
                ('partidos_perdidos', models.IntegerField(default=0)),
                ('set_favor', models.IntegerField(default=0)),
                ('set_contra', models.IntegerField(default=0)),
                ('puntos_favor', models.IntegerField(default=0)),
                ('puntos_contra', models.IntegerField(default=0)),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Equipo')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Grupo')),
            ],
            options={
                'ordering': ['-partidos_ganados', '-set_favor', '-puntos_favor', 'puntos_contra'],
            },
        ),
        migrations.AddField(
            model_name='campo',
            name='fase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Fase'),
        ),
        migrations.CreateModel(
            name='Ascenso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_equipos', models.IntegerField()),
                ('desde_posicion', models.IntegerField()),
                ('UPD', models.DateTimeField(auto_now=True)),
                ('NWD', models.DateTimeField(auto_now_add=True)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Grupo')),
                ('proxima_fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubogt.Fase')),
            ],
        ),
    ]
