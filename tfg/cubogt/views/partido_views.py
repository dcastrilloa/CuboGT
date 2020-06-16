from django.shortcuts import render, get_object_or_404, redirect

from cubogt.forms import PartidoResultadoForm, \
	SetJuegosForm, SetPuntosForm
from ..controller import FaseController, PartidoController, SetController, ClasificacionController
from ..models import Torneo, Fase, Partido, Campo, Grupo, Set
from ..static.constantes import ESPERA, JUGANDO


def partido_enjuego(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	partido_list = PartidoController.get_partidos_jugando_list(fase)
	partido_campo_proximos_list = PartidoController.get_partidos_con_campos_para_forzar(fase)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'fase': fase,
			   'partido_list': partido_list, 'partido_campo_proximos_list': partido_campo_proximos_list}
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


def partido_ver(request, torneo_id, fase_id, grupo_id, partido_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	partido = get_object_or_404(Partido, pk=partido_id, grupo=grupo)
	set_list = Set.objects.filter(partido=partido)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'fase': fase, 'grupo': grupo,
			   'partido': partido, 'set_list': set_list}
	return render(request, 'cubogt/fase_activa/partido/partido_ver.html', context)


def partido_editar_resultado(request, torneo_id, fase_id, grupo_id, partido_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	partido = get_object_or_404(Partido, pk=partido_id, grupo=grupo)

	if request.method == "POST":
		form = PartidoResultadoForm(request.POST, instance=partido)
		if form.is_valid():
			partido = form.save(commit=False)
			partido.ganador = PartidoController.get_equipo_ganador(partido)
			partido.save()
			# Actualizo Clasificación
			ClasificacionController.actualizar_clasificacion(partido)

			return redirect('partido_ver', torneo_id=torneo.id, fase_id=fase_id, grupo_id=grupo_id,
							partido_id=partido_id)
	else:
		form = PartidoResultadoForm(instance=partido)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/fase_activa/partido/partido_editar_resultado.html', context)


def partido_set_nuevo(request, torneo_id, fase_id, grupo_id, partido_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	partido = get_object_or_404(Partido, pk=partido_id, grupo=grupo)

	if request.method == "POST":
		if torneo.deporte.juego:
			form = SetJuegosForm(request.POST)
		else:
			form = SetPuntosForm(request.POST, fase=fase)
		if form.is_valid():
			set_partido = form.save(commit=False)
			set_partido.partido = partido
			set_partido.numero_set = Set.objects.filter(partido=partido).count() + 1
			set_partido.ganador = SetController.get_equipo_ganador(set_partido)
			set_partido.save()
			# Compruebo el ganador del partido con el set añadido
			partido.ganador = PartidoController.get_equipo_ganador(partido)
			partido.save()
			# Actualizo Clasificación
			ClasificacionController.actualizar_clasificacion(partido)
			return redirect('partido_ver', torneo_id=torneo.id, fase_id=fase_id, grupo_id=grupo_id,
							partido_id=partido_id)
	else:
		if torneo.deporte.juego:
			form = SetJuegosForm()
		else:
			form = SetPuntosForm(fase=fase)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/fase_activa/partido/partido_set_nuevo.html', context)


def partido_set_editar(request, torneo_id, fase_id, grupo_id, partido_id, set_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	partido = get_object_or_404(Partido, pk=partido_id, grupo=grupo)
	set_partido = get_object_or_404(Set, pk=set_id, partido=partido)

	if request.method == "POST":
		if torneo.deporte.juego:
			form = SetJuegosForm(request.POST, instance=set_partido)
		else:
			form = SetPuntosForm(request.POST, instance=set_partido, fase=fase)
		if form.is_valid():
			set_partido = form.save(commit=False)
			set_partido.ganador = SetController.get_equipo_ganador(set_partido)
			set_partido.save()
			# Compruebo el ganador del partido con los cambios de set
			partido.ganador = PartidoController.get_equipo_ganador(partido)
			partido.save()
			# Actualizo Clasificación
			ClasificacionController.actualizar_clasificacion(partido)

			return redirect('partido_ver', torneo_id=torneo.id, fase_id=fase_id, grupo_id=grupo_id,
							partido_id=partido_id)
	else:
		if torneo.deporte.juego:
			form = SetJuegosForm(instance=set_partido)
		else:
			form = SetPuntosForm(instance=set_partido, fase=fase)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/fase_activa/partido/partido_set_editar.html', context)


def partido_set_borrar(request, torneo_id, fase_id, grupo_id, partido_id, set_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	partido = get_object_or_404(Partido, pk=partido_id, grupo=grupo)
	set_partido = get_object_or_404(Set, pk=set_id, partido=partido)

	set_partido.delete()
	# Compruebo el ganador del partido con el set borrado
	partido.ganador = PartidoController.get_equipo_ganador(partido)
	partido.save()
	# Actualizo Clasificación
	ClasificacionController.actualizar_clasificacion(partido)

	return redirect('partido_ver', torneo_id=torneo.id, fase_id=fase_id, grupo_id=grupo_id,
					partido_id=partido_id)


def partido_terminar(request, torneo_id, fase_id, grupo_id, partido_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	partido = get_object_or_404(Partido, pk=partido_id, grupo=grupo)

	PartidoController.partido_terminar(partido)
	return redirect('partido_enjuego', torneo_id=torneo_id, fase_id=fase_id)


def partido_calendario_grupo(request, torneo_id, fase_id, grupo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	if grupo_id:
		grupo_actual = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	else:
		grupo_actual = fase.grupo_set.first()

	grupo_list=fase.grupo_set.all()
	partido_list = PartidoController.get_partidos_jornadas_grupo(grupo_actual)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'fase': fase,
			   'grupo_list': grupo_list, 'partido_list': partido_list, 'grupo_actual': grupo_actual}
	return render(request, 'cubogt/fase_activa/calendario/calendario.html', context)


def partido_calendario(request, torneo_id, fase_id):
	return partido_calendario_grupo(request, torneo_id, fase_id, None)


def partido_calendario_grupo_especifico(request, torneo_id, fase_id, grupo_id, partido_id):
	return partido_calendario_grupo(request, torneo_id, fase_id, grupo_id)