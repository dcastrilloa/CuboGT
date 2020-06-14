from string import ascii_uppercase

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from cubogt.controller import PartidoController
from cubogt.models import Campo
from cubogt.static.constantes import JUGANDO, ABECEDARIO


def comprobar_campo(torneo):
	msg_error = []
	campo_list = Campo.objects.filter(torneo=torneo)
	if not campo_list:
		msg_error.append(_("Tienes que crear al menos un campo para poder iniciar el torneo.\n"))
	return msg_error


def get_campo_libre_list(fase):
	campo_libre_list = Campo.objects.filter(fase=fase).exclude(partido__estado=JUGANDO)
	return campo_libre_list


def get_campo_fase_list(fase):
	campo_libre_list = Campo.objects.filter(fase=fase)
	return campo_libre_list


def get_campos_para_forzar(fase):
	"""Devuelve una lista con Query de los campos donde se podrian forzar los partidos en espera"""
	partidos_espera_list = PartidoController.get_partidos_espera_list(fase)
	campos_fase = get_campo_fase_list(fase)
	campo_list = []
	for partido_espera in partidos_espera_list:
		campo_aux_local = campos_fase \
			.filter(Q(partido__equipo_local=partido_espera.equipo_local) |
					Q(partido__equipo_visitante=partido_espera.equipo_local), partido__estado=JUGANDO)
		campo_aux_visitante = campos_fase \
			.filter(Q(partido__equipo_local=partido_espera.equipo_visitante) |
					Q(partido__equipo_visitante=partido_espera.equipo_visitante), partido__estado=JUGANDO)
		if campo_aux_local and campo_aux_visitante:
			campo_list.append([])
		elif campo_aux_local:
			campo_list.append([campo_aux_local])
		elif campo_aux_visitante:
			campo_list.append([campo_aux_visitante])
		else:
			campo_list.append(campos_fase)

	return campo_list


def generar_campos(torneo, numero_campos, tipo_nombre):
	if tipo_nombre == ABECEDARIO:
		for x in range(numero_campos):
			nombre = "Campo " + ascii_uppercase[x]
			nuevo_campo(torneo, nombre)
	else:
		for x in range(1, numero_campos + 1):
			nombre = "Campo " + str(x)
			nuevo_campo(torneo, nombre)


def nuevo_campo(torno, nombre):
	campo = Campo(torneo=torno, nombre=nombre)
	campo.save()
