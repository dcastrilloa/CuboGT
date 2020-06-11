from cubogt.models import Grupo, Equipo, Fase, Ascenso
from . import GrupoController, EquipoController, TorneoController, AscensoController
from cubogt.static.constantes import CREACION


def fase_iniciar(fase):
	# TODO crear calendario
	# TODO cambiar el torneo a estado ACTIVO
	# TODO cambiar la fase a estado ACTIVO
	# TODO elegir los campos donde se va a jugar
	pass


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
