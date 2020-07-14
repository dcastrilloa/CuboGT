from cubogt.models import Grupo, Fase, Campo
from cubogt.static.constantes import CREACION, ACTIVO, TERMINADO, ELIMINATORIA, NUMEROS, NOMBRE_ELIMINATORIA, \
	TERCER_PUESTO
from . import GrupoController, EquipoController, TorneoController, AscensoController, PartidoController, CampoController


def fase_iniciar(fase):
	if fase.tipo_fase == ELIMINATORIA:
		fase_iniciar_eliminatoria(fase)
	# crear calendario
	PartidoController.crear_calendario(fase)
	# cambiar el torneo a estado ACTIVO
	torneo = fase.torneo
	if torneo.estado != ACTIVO:
		torneo.estado = ACTIVO
		torneo.save()
	# cambiar la fase a estado ACTIVO y asignar un numero de activacion
	fase.estado = ACTIVO
	fase.numero_activacion = Fase.objects.filter(torneo=torneo, numero_activacion__isnull=False).count()
	fase.save()
	iniciar_siguiente_partido(fase)


def fase_iniciar_eliminatoria(fase):
	numero_grupos = GrupoController.get_numero_grupos(fase)

	# Si no tengo grupos: crear grupos (nombre eliminatoria) y repartirlos
	if not numero_grupos:
		numero_grupos = GrupoController.get_numero_grupos_crear_eliminatoria(fase)
		GrupoController.generar_grupos(fase, numero_grupos, NUMEROS, eliminatoria=True)
		GrupoController.repartir_equipos(fase)

	# Añado el nombre de la eliminatoria a fase.
	fase.nombre = fase.prefijo_eliminatoria + NOMBRE_ELIMINATORIA[numero_grupos]


def fase_terminar(fase):
	if fase.tipo_fase == ELIMINATORIA:
		fase_eliminatoria_terminar(fase)
	# cambiar la fase a estado TERMINADO
	fase.estado = TERMINADO
	fase.save()
	# comprobar si el torneo esta TERMINADO
	torneo = fase.torneo
	TorneoController.comprobar_terminar_torneo(torneo)
	# llamar a ascenso
	AscensoController.realizar_ascenso_fase(fase)


def fase_eliminatoria_terminar(fase):
	numero_grupos = GrupoController.get_numero_grupos(fase)
	# Si tengo mas de dos equipos(1 grupo): crear FASE SIGUIENTE y el ascenso del primero de cada grupo
	if numero_grupos > 1:
		# Crear fase siguiente
		nombre_fase_siguiente = fase.prefijo_eliminatoria + NOMBRE_ELIMINATORIA[numero_grupos//2]
		fase_siguiente = Fase(torneo=fase.torneo, nombre=nombre_fase_siguiente,
							  prefijo_eliminatoria=fase.prefijo_eliminatoria, tipo_fase=ELIMINATORIA,
							  numero_equipos_max=numero_grupos , doble_partido=fase.doble_partido,
							  numero_sets=fase.numero_sets, numero_puntos=fase.numero_puntos,
							  puntos_maximos=fase.puntos_maximos)
		fase_siguiente.save()
		fase_siguiente.campos.add(*fase.campos.all())

		# Ascenso
		AscensoController.ascenso_general(fase, numero_equipos=1, desde_posicion=1, proxima_fase=fase_siguiente)

		# Tercer y cuarto puesto
		if numero_grupos == 2 and fase.equipos.count() == 4:
			nombre_fase_siguiente = fase.prefijo_eliminatoria + NOMBRE_ELIMINATORIA[TERCER_PUESTO]
			fase_siguiente_3 = Fase(torneo=fase.torneo, nombre=nombre_fase_siguiente,
								  prefijo_eliminatoria=fase.prefijo_eliminatoria, tipo_fase=ELIMINATORIA,
								  numero_equipos_max=numero_grupos, doble_partido=fase.doble_partido,
								  numero_sets=fase.numero_sets, numero_puntos=fase.numero_puntos,
								  puntos_maximos=fase.puntos_maximos)
			fase_siguiente_3.save()
			fase_siguiente_3.campos.add(*fase.campos.all())
			# Ascenso
			AscensoController.ascenso_general(fase, numero_equipos=1, desde_posicion=2, proxima_fase=fase_siguiente_3)



def fase_iniciar_comprobaciones(fase):
	msg_error = []
	# Comprobar Torneo
	if fase.torneo.estado == CREACION:
		msg_error.extend(TorneoController.comprobar_torneo(fase.torneo))
	# Comprobar los Equipos de la fase
	msg_error.extend(EquipoController.comprobar_equipos_fase(fase))
	# Comprobar los Grupo de la fase
	msg_error.extend(GrupoController.comprobar(fase))
	# Comprobar los Ascensos
	msg_error.extend(AscensoController.comprobar(fase))
	return msg_error


def get_fases_activas_terminadas(torneo):
	fases_activas_terminadas = Fase.objects.filter(torneo=torneo).exclude(estado=CREACION)
	return fases_activas_terminadas


def iniciar_siguiente_partido(fase, arbitro=None):
	partido_sin_terminar = PartidoController.get_partidos_no_terminados_list(fase)
	partido_jugable_list = PartidoController.get_partidos_espera_equipos_no_jugando_list(fase)
	campo_libre_list = CampoController.get_campo_libre_list(fase)
	if not partido_sin_terminar:
		fase_terminar(fase)
	elif partido_jugable_list and campo_libre_list:
		partido = partido_jugable_list.first()
		campo = campo_libre_list.first()
		PartidoController.set_partido_jugar(partido, campo, arbitro)
		iniciar_siguiente_partido(fase)


def borrar_equipo_de_fase(fase, equipo):
	"""Busca un grupo de la fase y borra la relacion con el equipo"""
	grupo_list = Grupo.objects.filter(fase=fase, equipos=equipo)
	if grupo_list:
		GrupoController.borrar_equipo(grupo_list.first(), equipo)
	fase.equipos.remove(equipo)


def fase_equipo_borrar_todo(fase):
	grupos_list = fase.grupo_set.all()
	for grupo in grupos_list:
		grupo.equipos.clear()
	fase.equipos.clear()


def fase_equipo_nuevo(fase, equipo):
	fase.equipos.add(equipo)
	fase.save()


def fase_equipo_agregar_ascenso(fase):
	fase_equipo_borrar_todo(fase)
	AscensoController.recibir_ascenso(fase)
