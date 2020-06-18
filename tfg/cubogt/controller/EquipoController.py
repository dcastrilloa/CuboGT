from django.utils.translation import gettext_lazy as _

from cubogt.models import Equipo, Fase
from cubogt.static.constantes import ACTIVO


def comprobar_equipos_torneo(torneo):
	msg_error = []
	equipo_list = Equipo.objects.filter(torneo=torneo)
	if len(equipo_list) < 2:
		msg_error.append(_("No hay suficientes equipos en el torneo para poder iniciarlo, se necesitan al menos 2.\n"))
	return msg_error


def comprobar_equipos_fase(fase):
	msg_error = []
	equipo_list = Equipo.objects.filter(fase=fase)
	if len(equipo_list) < 2:
		msg_error.append(_("No hay suficientes equipos en la fase para poder iniciarla, se necesitan al menos 2.\n"))
	else:  # comprobar que no haya equipos repetidos en otra fase ACTIVO
		otras_fases_activas = Fase.objects.filter(torneo=fase.torneo, estado=ACTIVO).exclude(id=fase.id)
		equipos_repetidos = equipo_list.filter(fase__in=otras_fases_activas)
		if equipos_repetidos:
			for equipo in equipos_repetidos:
				fase_equipo = Fase.objects.get(estado=ACTIVO, equipos=equipo)
				msg_error.append(_("El equipo: %(equipo)s ya esta jugando en otra fase activa: %(fase)s\n") %
								 {'equipo': equipo.nombre, 'fase': fase_equipo.nombre})
	return msg_error
