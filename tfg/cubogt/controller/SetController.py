from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import FaseForm, FasePuntoForm, FaseSetForm, FaseEquipoForm, PartidoResultadoForm, \
	SetJuegosForm, SetPuntosForm
from ..controller import GrupoController, FaseController, PartidoController, CampoController
from ..models import Torneo, Fase, Equipo, Partido, Campo, Grupo, Set
from ..static.constantes import ESPERA, JUGANDO, TERMINADO


def get_equipo_ganador(set_partido):
	deporte = set_partido.partido.grupo.fase.torneo.deporte
	partido = set_partido.partido
	ganador = None
	if deporte.juego:
		if set_partido.juegos_local > set_partido.juegos_visitante:
			ganador = partido.equipo_local
		elif set_partido.juegos_local < set_partido.juegos_visitante:
			ganador = partido.equipo_visitante
	else:
		if set_partido.puntos_local > set_partido.puntos_visitante:
			ganador = partido.equipo_local
		elif set_partido.puntos_local < set_partido.puntos_visitante:
			ganador = partido.equipo_visitante

	return ganador
