from cubogt.models import Fase
from . import EquipoController, CampoController
from ..static.constantes import TERMINADO


def comprobar_torneo(torneo):
	msg_error = []
	msg_error.extend(EquipoController.comprobar_equipos_torneo(torneo))
	msg_error.extend(CampoController.comprobar_campo(torneo))
	return msg_error


def comprobar_terminar_torneo(torneo):
	fases_no_terminadas = Fase.objects.filter(torneo=torneo).exclude(estado=TERMINADO)
	if not fases_no_terminadas:
		torneo_terminar(torneo)


def torneo_terminar(torneo):
	torneo.estado = TERMINADO
	torneo.save()
