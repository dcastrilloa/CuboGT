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
	numero_activacion = models.IntegerField(null=True, default=None)
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

	class Meta:
		ordering = ["numero_activacion", "nombre"]

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
			label = _("%(n_equipos)sIndefinido" % {'n_equipos': label})
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
		ordering = ["-partidos_ganados", "-partidos_empatados", "-sets_favor", "-sets_contra",
					"-juegos_favor","-juegos_contra","-puntos_favor", "puntos_contra"]

	def __str__(self):
		return '(%s - %s)' % (self.equipo, self.get_puntuacion())

	def get_puntuacion(self):
		ganado = 3
		empatado = 1
		return self.partidos_ganados * ganado+self.partidos_empatados*empatado


class Ascenso(models.Model):
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	numero_equipos = models.IntegerField()
	desde_posicion = models.IntegerField()
	proxima_fase = models.ForeignKey('Fase', on_delete=models.CASCADE)

	estado = models.IntegerField(choices=ESTADO_ASCENSO_CHOICES, default=ESPERA)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["grupo"]

	def posiciones_label(self):
		aux = ""
		for x in range(self.desde_posicion, self.desde_posicion + self.numero_equipos):
			aux += str(x) + ","
		return aux[:-1]

	def get_posiciones_array(self):
		posiciones = []
		for x in range(self.desde_posicion, self.desde_posicion + self.numero_equipos):
			posiciones.append(x)
		return posiciones


class Partido(models.Model):
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	equipo_local = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="local_equipo")
	equipo_visitante = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="visitante_equipo")
	arbitro = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="arbitro", null=True, default=None)
	ganador = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="ganador", null=True, default=None)

	resultado_local = models.IntegerField(default=0)  # Fulbol, baloncesto, waterpolo...
	resultado_visitante = models.IntegerField(default=0)  # Fulbol, baloncesto, waterpolo...

	campo = models.ForeignKey('Campo', on_delete=models.CASCADE, null=True)
	jornada = models.IntegerField()
	estado = models.IntegerField(choices=ESTADO_PARTIDO_CHOICES, default=ESPERA)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["jornada", "grupo"]

	def __str__(self):
		return '%s - %s' % (self.equipo_local, self.equipo_visitante)

	def get_numero_sets_local(self):
		return Set.objects.filter(partido=self, ganador=self.equipo_local).count()

	def get_numero_sets_visitante(self):
		return Set.objects.filter(partido=self, ganador=self.equipo_visitante).count()

	def get_resultado_label(self):
		if self.grupo.fase.torneo.deporte.set:
			sets_local = self.get_numero_sets_local()
			sets_visitante = self.get_numero_sets_visitante()
			label = '%d - %d' % (sets_local, sets_visitante)
		else:
			label = '%d - %d' % (self.resultado_local, self.resultado_visitante)
		return label

	def get_arbitro_label(self):
		if self.arbitro:
			label = self.arbitro.nombre
		else:
			label = _("Organización")
		return label


class Set(models.Model):
	partido = models.ForeignKey('Partido', on_delete=models.CASCADE)
	numero_set = models.IntegerField()
	ganador = models.ForeignKey('Equipo', on_delete=models.CASCADE, null=True, default=None)

	puntos_local = models.IntegerField(default=0)  # Voleibol, Pinpong, Batminton...
	puntos_visitante = models.IntegerField(default=0)  # Voleibol, Pinpong, Batminton...
	juegos_local = models.IntegerField(default=0)  # Solo los uso si lo meto a mano
	juegos_visitante = models.IntegerField(default=0)  # Solo los uso si lo meto a mano

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_set"]

	def __str__(self):
		label = _("Set %(numero_set)d") % {'numero_set': self.numero_set}
		return label


class Juego(models.Model):
	set = models.ForeignKey('Set', on_delete=models.CASCADE)
	numero_juego = models.IntegerField()
	ganador = models.ForeignKey('Equipo', on_delete=models.CASCADE, null=True, default=None)

	puntos_local = models.IntegerField(default=0)
	puntos_visitante = models.IntegerField(default=0)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_juego"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.numero_juego = Juego.objects.filter(set=self.set).count() + 1

	def __str__(self):
		return _("Juego %(numero_juego)d") % {'numero_juego': self.numero_juego}


class Campo(models.Model):
	torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50)
	libre = models.BooleanField(default=True)  # No la uso

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre
