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
		crear_eliminatoria(fase)
	grupo_list= Grupo.objects.filter(fase=fase)
	for grupo in grupo_list:
		rondas=get_rondas()
		calendario_list = crear_lista_calendario(grupo,)


def crear_lista_partidos(teams, rounds):
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
