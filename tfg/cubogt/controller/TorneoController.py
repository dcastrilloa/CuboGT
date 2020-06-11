from django.utils.translation import gettext_lazy as _
from cubogt.models import Torneo
from . import EquipoController, CampoController


def comprobar_torneo(torneo):
	msg_error = []
	msg_error.extend(EquipoController.comprobar_equipos_torneo(torneo))
	msg_error.extend(CampoController.comprobar_campo(torneo))
	return msg_error
