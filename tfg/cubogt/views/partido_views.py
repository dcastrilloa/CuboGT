from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import FaseForm, FasePuntoForm, FaseSetForm, FaseEquipoForm
from ..controller import GrupoController, FaseController, PartidoController, CampoController
from ..models import Torneo, Fase, Equipo, Partido, Campo
from ..static.constantes import ESPERA, JUGANDO, TERMINADO


def partido_enjuego(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	partido_list = PartidoController.get_partido_jugando_list(fase)
	partido_campo_proximos_list = PartidoController.get_partidos_con_campos_para_forzar(fase)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'fase': fase,
			   'partido_list': partido_list, 'partido_campo_proximos_list':partido_campo_proximos_list }
	return render(request, 'cubogt/fase_activa/partido/partido_enjuego.html', context)


def partido_posponer(request, torneo_id, fase_id, partido_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	partido = get_object_or_404(Partido, pk=partido_id, estado=JUGANDO)
	PartidoController.partido_posponer(fase, partido)
	return redirect('partido_enjuego', torneo_id=torneo_id, fase_id=fase_id)


def partido_forzar(request, torneo_id, fase_id, partido_id, campo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	partido = get_object_or_404(Partido, pk=partido_id, grupo__fase=fase, estado=ESPERA)
	campo = get_object_or_404(Campo, pk=campo_id, fase=fase)

	PartidoController.partido_forzar(fase, partido, campo)
	return redirect('partido_enjuego', torneo_id=torneo_id, fase_id=fase_id)