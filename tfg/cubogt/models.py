from django.db import models


class Torneo(models.Model):
	nombre = models.CharField(max_length=100)
	deporte = models.ForeignKey('Deporte', on_delete=models.CASCADE)
	usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	estado = models.IntegerField()
	fecha = models.DateField()
	tipo_torneo = models.IntegerField()

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre


class Deporte (models.Model):
	nombre = models.CharField(max_length=100)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre


class Fase(models.Model):
	torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)
	fase_numero = models.IntegerField()
	# subfase_numero
	nombre = models.CharField(max_length=100, blank=True)
	numero_equipos = models.IntegerField()
	numero_grupos = models.IntegerField()
	numero_sets = models.IntegerField()
	numero_puntos = models.IntegerField()
	puntos_maximos = models.IntegerField(null=True, default=None)
	tipo_fase = models.IntegerField()
	doble_partid = models.BooleanField()
	cambio_de_campo = models.BooleanField()
	cambio_a_los = models.IntegerField(default=None)
	# puntuacion = models.ForeignKey('Puntuacion', on_delete=models.CASCADE)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombre


""" 
class Puntuacion(models.Model):
	ganado = models.IntegerField(default=3)
	perdido = models.IntegerField(default=0)
	empate  = models.IntegerField(default=1)
	ganado_max_set = models.IntegerField(default=blank)
	perdido_max_set = models.IntegerField(default=1)
	
	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)
"""


class Equipo(models.Model):
	torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	""" Para cuando este editando equipos quizas quiero que esten ordenados por ID
	class Meta:
		ordering = ["id"]
	"""
	def __str__(self):
		return self.nombre


class Grupo (models.Model):
	fase = models.ForeignKey('Fase', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50, blank=True, default=None)
	numero_grupo = models.IntegerField()

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_grupo"]

	def __str__(self):
		if self.nombre is None:
			return self.numero_grupo
		else:
			return self.nombre


class Clasificacion (models.Model):
	equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	partidos_jugados = models.IntegerField(default=0)
	partidos_ganados = models.IntegerField(default=0)
	partidos_perdidos = models.IntegerField(default=0)
	set_favor = models.IntegerField(default=0)
	set_contra = models.IntegerField(default=0)
	puntos_favor = models.IntegerField(default=0)
	puntos_contra = models.IntegerField(default=0)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-partidos_ganados", "-set_favor", "-puntos_favor", "puntos_contra"]

	def __str__(self):
		return '(%s - %s)' % (self.equipo, self.get_puntuacion())

	def get_puntuacion(self):
		ganado = 3
		return self.partidos_ganados*ganado


class Campo (models.Model):
	fase = models.ForeignKey('Fase', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50, blank=True, default=None)
	numero_campo = models.IntegerField()
	cubo = models.GenericIPAddressField(blank=True, null=True, default=None)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.nombre is None:
			return self.numero_campo
		else:
			return self.nombre


class Partido (models.Model):
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	equipo_local = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="local_equipo")
	equipo_visitante = models.ForeignKey('Equipo', on_delete=models.CASCADE, related_name="visitante_equipo")
	resultado_local = models.IntegerField()
	resultado_visitante = models.IntegerField()
	campo = models.ForeignKey('Campo', on_delete=models.CASCADE)
	jornada = models.IntegerField()
	esta_terminado = models.BooleanField()
	es_eliminatoria = models.BooleanField()

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s - %s' % (self.equipo_local, self.equipo_visitante)


class SetVoleibol (models.Model):
	partido = models.ForeignKey('Partido', on_delete=models.CASCADE)
	numero_set = models.IntegerField()
	puntos_local = models.IntegerField()
	puntos_visitante = models.IntegerField()

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["numero_set"]

	def __str__(self):
		return '(%s - %s)' % (self.puntos_local, self.puntos_visitante)


class Ascenso (models.Model):
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	numero_equipos = models.IntegerField()
	desde_posicion = models.IntegerField()
	proxima_fase = models.ForeignKey('Fase', on_delete=models.CASCADE)

	UPD = models.DateTimeField(auto_now=True)
	NWD = models.DateTimeField(auto_now_add=True)