from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import FaseForm, FasePuntoForm, FaseSetForm, FaseEquipoForm
from ..controller import GrupoController
from ..models import Torneo, Fase, Equipo, Partido, Campo, Grupo
from ..static.constantes import LIGA, ELIMINATORIA


def a():
	# campo= Campo.objects.filter(fase=fase).exclude(partido__estado=ACTIVO)
	# campo=Campo.objects.filter(fase=fase,libre=True)
	pass


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
		rondas *=2
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
	for jornada in range(1, len(calendario_list)+1):
		for enfrentamiento in calendario_list[jornada-1]:
			if enfrentamiento[0] and enfrentamiento[1]:
				if doble_partido and jornada > (len(calendario_list) / 2):
					Partido.objects.create(grupo=grupo, equipo_local=enfrentamiento[1],
										   equipo_visitante=enfrentamiento[0],
										   jornada=jornada)
				else:
					Partido.objects.create(grupo=grupo, equipo_local=enfrentamiento[0],
										   equipo_visitante=enfrentamiento[1],
										   jornada=jornada)
