from django.utils.translation import gettext_lazy as _
from cubogt.models import Grupo, Equipo, Fase, Ascenso


def comprobar_equipos_torneo(torneo):
	msg_error=[]
	equipo_list = Equipo.objects.filter(torneo=torneo)
	if len(equipo_list) < 2:
		msg_error.append(_("No hay suficientes equipos en el torneo para poder iniciarlo, se necesitan al menos 2\n"))
	return msg_error


def comprobar_equipos_fase(fase):
	msg_error = []
	equipo_list = Equipo.objects.filter(fase=fase)
	if len(equipo_list) < 2:
		msg_error.append(_("No hay suficientes equipos en la fase para poder iniciarla, se necesitan al menos 2\n"))
	return msg_error
