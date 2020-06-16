from cubogt.models import Grupo, Equipo, Fase, Ascenso, Partido, Campo
from . import GrupoController, EquipoController, TorneoController, AscensoController, PartidoController, CampoController
from cubogt.static.constantes import CREACION, ACTIVO, ESPERA, TERMINADO


def fase_iniciar(fase):
	# crear calendario
	PartidoController.crear_calendario(fase)
	# cambiar el torneo a estado ACTIVO
	torneo = fase.torneo
	if torneo.estado == CREACION:
		torneo.estado = ACTIVO
		torneo.save()
	# cambiar la fase a estado ACTIVO y asignar un numero de activacion
	fase.estado = ACTIVO
	fase.numero_activacion = Fase.objects.filter(torneo=torneo, numero_activacion__isnull=False).count()
	fase.save()


def fase_terminar(fase):
	# cambiar la fase a estado TERMINADO
	fase.estado = TERMINADO
	fase.save()
	# comprobar si el torneo esta TERMINADO
	torneo = fase.torneo
	TorneoController.terminar_torneo(torneo)
	# Todo llamar a ascenso


def fase_iniciar_comprobaciones(fase):
	msg_error = []
	# Comprobar Torneo
	if fase.torneo.estado is CREACION:
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
