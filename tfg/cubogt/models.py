from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from cubogt.static.constantes import *
from django.shortcuts import redirect


class Deporte(models.Model):
	nombre = models.CharField(max_length=15, choices=DeporteChoices.choices, default=DeporteChoices.VOLEIBOL)
	juego = models.BooleanField()
	set = models.BooleanField()
	punto = models.BooleanField(default=False)

	class Meta:
		ordering = ["nombre"]

	def __str__(self):
		return self.get_nombre_display()


class Torneo(models.Model):
	equipos = models.ManyToManyField('Equipo')
	deporte = models.ForeignKey('Deporte', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=100)

	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	estado = models.IntegerField(choices=ESTADO_CHOICES, default=CREACION)
	fecha = models.DateField()
	descripcion = models.CharField(max_length=255, blank=True)
	numero_equipos_max = models.IntegerField(null=True, blank=True)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["fecha"]

	def __str__(self):
		return self.nombre


class Fase(models.Model):
	torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)
	equipos = models.ManyToManyField('Equipo')
	campos = models.ManyToManyField('Campo')
	# fase_numero = models.IntegerField()
	nombre = models.CharField(max_length=100)
	tipo_fase = models.IntegerField(choices=TIPO_FASE)
	numero_equipos_max = models.IntegerField(null=True, blank=True)
	doble_partido = models.BooleanField()

	numero_sets = models.IntegerField(null=True)
	numero_puntos = models.IntegerField(null=True)
	puntos_maximos = models.IntegerField(null=True, blank=True)
	# cambio_de_campo = models.BooleanField()
	# cambio_a_los = models.IntegerField(default=None)

	estado = models.IntegerField(choices=ESTADO_CHOICES, default=CREACION)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre

	def doble_partido_label(self):
		if self.doble_partido:
			return _("Si")
		else:
			return _("No")

	def equipos_apuntados_max_label(self):
		label = str(self.equipos.count()) + "/"
		if self.numero_equipos_max is not None and self.numero_equipos_max > 0:
			label += str(self.numero_equipos_max)
		else:
			label += _("Indefinido")
		return label


class Equipo(models.Model):
	nombre = models.CharField(max_length=50)
	correo = models.EmailField(max_length=50)
	integrantes = models.ManyToManyField(User, through='Jugador')

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["nombre"]

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
	nombre = models.CharField(max_length=50)
	equipos = models.ManyToManyField('Equipo', through='Clasificacion')
	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["nombre"]

	def __str__(self):
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

	class Meta:
		ordering = ["grupo"]

	def posiciones_label(self):
		aux = ""
		for x in range(self.desde_posicion, self.desde_posicion + self.numero_equipos):
			aux += str(x) + ","
		return aux[:-1]


class Partido(models.Model):
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	equipo_local = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="local_equipo")
	equipo_visitante = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="visitante_equipo")
	arbitro = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="arbitro", null=True, default=None)

	sets_favor = models.IntegerField(default=0)
	sets_contra = models.IntegerField(default=0)
	juegos_favor = models.IntegerField(default=0)
	juegos_contra = models.IntegerField(default=0)
	puntos_favor = models.IntegerField(default=0)
	puntos_contra = models.IntegerField(default=0)

	campo = models.ForeignKey('Campo', on_delete=models.CASCADE)
	jornada = models.IntegerField()
	estado = models.IntegerField(choices=ESTADO_PARTIDO_CHOICES, default=ESPERA)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s - %s' % (self.equipo_local, self.equipo_visitante)


class Set(models.Model):
	partido = models.ForeignKey('Partido', on_delete=models.CASCADE)
	numero_set = models.IntegerField()
	puntos_local = models.IntegerField(default=0)
	puntos_visitante = models.IntegerField(default=0)
	juegos_local = models.IntegerField(default=0)
	juegos_visitante = models.IntegerField(default=0)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_set"]

	def __str__(self):
		return '(%s - %s)' % (self.puntos_local, self.puntos_visitante)


class Juego(models.Model):
	set = models.ForeignKey('Set', on_delete=models.CASCADE)
	numero_juego = models.IntegerField()
	puntos_local = models.IntegerField(default=0)
	puntos_visitante = models.IntegerField(default=0)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_juego"]

	def __str__(self):
		return '(%s - %s)' % (self.puntos_local, self.puntos_visitante)


class Campo(models.Model):
	torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50)
	libre = models.BooleanField(default=True)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre
