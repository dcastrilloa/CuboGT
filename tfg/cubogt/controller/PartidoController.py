from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import FaseForm, FasePuntoForm, FaseSetForm, FaseEquipoForm
from . import CampoController
from ..controller import GrupoController
from ..models import Torneo, Fase, Equipo, Partido, Campo, Grupo
from ..static.constantes import LIGA, ELIMINATORIA, JUGANDO, ESPERA, TERMINADO


def crear_calendario(fase):
	if fase.tipo_fase is LIGA:
		crear_liga(fase)
	else:
		# TODO crear_eliminatoria(fase)
		pass


def crear_liga(fase):
	grupo_list = Grupo.objects.filter(fase=fase)
	for grupo in grupo_list:
		rondas = calcular_rondas(fase, grupo)
		equipos_list = grupo.equipos.all()
		calendario_grupo_list = crear_lista_partidos(list(equipos_list), rondas)
		crear_partido_lista(grupo, calendario_grupo_list, fase.doble_partido)


def calcular_rondas(fase, grupo):
	n_equipos = grupo.equipos.count()
	if (n_equipos % 2) == 0:
		rondas = n_equipos - 1
	else:
		rondas = n_equipos
	if fase.doble_partido:
		rondas *= 2
	return rondas


def crear_lista_partidos(teams, rounds):
	"""Devuelve una lista de listas de jornadas, dentro de esa lista de jornadas hay una tupla con los enfrentamientos
	equipo_local vs equipo_visitante"""
	if len(teams) % 2:
		teams.append(None)

	schedule = []
	for turn in range(rounds):
		pairings = []
		for i in range(int(len(teams) / 2)):
			pairings.append((teams[i], teams[len(teams) - i - 1]))
		teams.insert(1, teams.pop())
		schedule.append(pairings)

	return schedule


def crear_partido_lista(grupo, calendario_list, doble_partido):
	for jornada in range(1, len(calendario_list) + 1):
		for enfrentamiento in calendario_list[jornada - 1]:
			if enfrentamiento[0] and enfrentamiento[1]:
				if doble_partido and jornada > (len(calendario_list) / 2):
					Partido.objects.create(grupo=grupo, equipo_local=enfrentamiento[1],
										   equipo_visitante=enfrentamiento[0],
										   jornada=jornada)
				else:
					Partido.objects.create(grupo=grupo, equipo_local=enfrentamiento[0],
										   equipo_visitante=enfrentamiento[1],
										   jornada=jornada)


def iniciar_partido(partido, campo):
	partido.campo = campo
	partido.estado = JUGANDO
	partido.save()


def get_partidos_jugando_list(fase):
	partidos_jugando = Partido.objects.filter(grupo__fase=fase, estado=JUGANDO)
	return partidos_jugando


def get_partidos_espera_list(fase):
	partidos_espera = Partido.objects.filter(grupo__fase=fase, estado=ESPERA)
	return partidos_espera


def get_partidos_no_terminados_list(fase):
	partidos_espera = Partido.objects.filter(grupo__fase=fase, estado__lt=TERMINADO)
	return partidos_espera


def get_partidos_espera_equipos_no_jugando_list(fase):
	"""Devuelve una lista con los partidos que se pueden jugar sin que coincida alguno que este en juego"""
	partidos_espera_list = get_partidos_espera_list(fase)
	partidos_jugando_list = get_partidos_jugando_list(fase)
	equipos_jugando = []
	for partido_jugando in partidos_jugando_list:
		equipos_jugando.append(partido_jugando.equipo_local)
		equipos_jugando.append(partido_jugando.equipo_visitante)
	partidos_espera_equipos_no_jugando_list = partidos_espera_list.exclude(equipo_local__in=equipos_jugando) \
		.exclude(equipo_visitante__in=equipos_jugando)
	return partidos_espera_equipos_no_jugando_list


def get_partidos_con_campos_para_forzar(fase):
	"""Devuelve una lista de listas con los partidos que se pueden jugar en los campos disponibles
	[[partido,[campo,campo]],[partido,[campo]],[partido,[]]...]"""
	partidos_espera_list = get_partidos_espera_list(fase)
	campos_para_forzar_list = CampoController.get_campos_para_forzar(fase)
	partido_campo = []
	for x in range(0,len(partidos_espera_list)):
		aux = [partidos_espera_list[x], campos_para_forzar_list[x]]
		partido_campo.append(aux)
	return partido_campo


def get_partido_jugando_list(fase):
	partido_jugando_list = Partido.objects.filter(grupo__fase=fase, estado=JUGANDO)
	return partido_jugando_list


def set_partido_posponer(partido):
	partido.estado = ESPERA
	partido.save()


def partido_posponer(fase, partido):
	set_partido_posponer(partido)
	campo = partido.campo
	campo_list = CampoController.get_campo_fase_list(fase)
	if campo in campo_list:
		partidos_espera_list = get_partidos_espera_equipos_no_jugando_list(fase).exclude(pk=partido.id)
		if partidos_espera_list:
			partido_siguiente = partidos_espera_list.first()
			iniciar_partido(partido_siguiente, campo)
		else: # No se puede posponer el partido
			iniciar_partido(partido, campo)


def partido_forzar(fase, partido, campo):
	partido_reemplazar = Partido.objects.get(grupo__fase=fase, campo=campo, estado=JUGANDO)
	set_partido_posponer(partido_reemplazar)

	iniciar_partido(partido, campo)
