from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from cubogt.controller.constantes import *


class Torneo(models.Model):
	nombre = models.CharField(max_length=100)

	deporte = models.CharField(max_length=15, choices=Deporte.choices, default=Deporte.VOLEIBOL)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	estado = models.IntegerField(choices=ESTADO_TORNEO_CHOICES, default=CREACION)
	fecha = models.DateField()
	descripcion = models.CharField(max_length=255, blank=True)
	numero_equipos = models.IntegerField(null=True)
	equipos = models.ManyToManyField('Equipo')

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre


class Fase(models.Model):
	torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)
	equipos = models.ManyToManyField('Equipo')
	campos = models.ManyToManyField('Campo')
	fase_numero = models.IntegerField()
	nombre = models.CharField(max_length=100, null=True)
	numero_equipos = models.IntegerField(null=True)
	numero_grupos = models.IntegerField(default=0)
	numero_sets = models.IntegerField(null=True)
	numero_puntos = models.IntegerField(null=True)
	puntos_maximos = models.IntegerField(null=True)
	tipo_fase = models.IntegerField()
	doble_partid = models.BooleanField()
	# cambio_de_campo = models.BooleanField()
	# cambio_a_los = models.IntegerField(default=None)
	esta_terminada = models.BooleanField(default=False)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.nombre is None:
			return self.fase_numero
		else:
			return self.nombre


class Equipo(models.Model):
	nombre = models.CharField(max_length=50)
	correo = models.EmailField(max_length=50)
	integrantes = models.ManyToManyField(User, through='Jugador')

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	""" Para cuando este editando equipos quizas quiero que esten ordenados por ID
	class Meta:
		ordering = ["id"]
	"""

	def __str__(self):
		return self.nombre


class Jugador(models.Model):
	equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha_incorporacion = models.DateTimeField(auto_now_add=True)
	fecha_salida = models.DateTimeField(null=True)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)


class Grupo(models.Model):
	fase = models.ForeignKey('Fase', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50, blank=True)
	numero_grupo = models.IntegerField()
	equipos = models.ManyToManyField('Equipo', through='Clasificacion')

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_grupo"]

	def __str__(self):
		if self.nombre is None:
			return self.numero_grupo
		else:
			return self.nombre


class Clasificacion(models.Model):
	equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	partidos_jugados = models.IntegerField(default=0)
	partidos_ganados = models.IntegerField(default=0)
	partidos_perdidos = models.IntegerField(default=0)
	partidos_empatados = models.IntegerField(default=0)

	sets_favor = models.IntegerField(default=0)
	sets_contra = models.IntegerField(default=0)
	juegos_favor = models.IntegerField(default=0)
	juegos_contra = models.IntegerField(default=0)
	puntos_favor = models.IntegerField(default=0)
	puntos_contra = models.IntegerField(default=0)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-partidos_ganados", "-sets_favor", "-puntos_favor", "puntos_contra"]

	def __str__(self):
		return '(%s - %s)' % (self.equipo, self.get_puntuacion())

	def get_puntuacion(self):
		ganado = 3
		return self.partidos_ganados * ganado


class Ascenso(models.Model):
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	numero_equipos = models.IntegerField()
	desde_posicion = models.IntegerField()
	proxima_fase = models.ForeignKey('Fase', on_delete=models.CASCADE)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)


class Partido(models.Model):
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	equipo_local = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="local_equipo")
	equipo_visitante = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="visitante_equipo")
	arbitro = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="arbitro")

	sets_favor = models.IntegerField(default=0)
	sets_contra = models.IntegerField(default=0)
	juegos_favor = models.IntegerField(default=0)
	juegos_contra = models.IntegerField(default=0)
	puntos_favor = models.IntegerField(default=0)
	puntos_contra = models.IntegerField(default=0)

	campo = models.ForeignKey('Campo', on_delete=models.CASCADE)
	jornada = models.IntegerField()
	esta_terminado = models.BooleanField(default=False)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s - %s' % (self.equipo_local, self.equipo_visitante)


class Set(models.Model):
	partido = models.ForeignKey('Partido', on_delete=models.CASCADE)
	numero_set = models.IntegerField()
	puntos_local = models.IntegerField(default=0)
	puntos_visitante = models.IntegerField(default=0)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_set"]

	def __str__(self):
		return '(%s - %s)' % (self.puntos_local, self.puntos_visitante)


class Campo(models.Model):
	torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50, blank=True)
	numero_campo = models.IntegerField()

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.nombre is None:
			return self.numero_campo
		else:
			return self.nombre
