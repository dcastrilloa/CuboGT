from cubogt.models import Grupo, Equipo, Fase, Ascenso
from . import GrupoController, EquipoController, TorneoController, AscensoController, PartidoController
from cubogt.static.constantes import CREACION, ACTIVO


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
